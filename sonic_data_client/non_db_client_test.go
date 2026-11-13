package client

import (
	"os"
	"path/filepath"
	"reflect"
	"testing"
	"unsafe"

	linuxproc "github.com/c9s/goprocinfo/linux"
)

const testProcStat = `cpu  1000 10 500 8000 50 0 20 0 0 0
cpu0 600 5 300 4000 30 0 10 0 0 0
cpu1 400 5 200 4000 20 0 10 0 0 0
intr 123456 1 2 3 4 5
ctxt 987654
btime 1700000000
processes 4321
procs_running 2
procs_blocked 0
softirq 5555 1 2 3
`

func readTestProcStat(t *testing.T, text string) *linuxproc.Stat {
	t.Helper()
	path := filepath.Join(t.TempDir(), "stat")
	if err := os.WriteFile(path, []byte(text), 0644); err != nil {
		t.Fatal(err)
	}
	stat, err := linuxproc.ReadStat(path)
	if err != nil {
		t.Fatal(err)
	}
	return stat
}

func TestNewCpuSample(t *testing.T) {
	stat := readTestProcStat(t, testProcStat)
	sample := newCpuSample(stat, nil)

	if want := (cpuTicks{total: 9580, idle: 8000}); sample.all != want {
		t.Errorf("all = %+v, want %+v", sample.all, want)
	}
	if want := []cpuTicks{{total: 4945, idle: 4000}, {total: 4635, idle: 4000}}; !reflect.DeepEqual(sample.cpus, want) {
		t.Errorf("cpus = %+v, want %+v", sample.cpus, want)
	}
	if sample.allId != "cpu" || !reflect.DeepEqual(sample.cpuIds, []string{"cpu0", "cpu1"}) {
		t.Errorf("ids = %q %q, want \"cpu\" [\"cpu0\" \"cpu1\"]", sample.allId, sample.cpuIds)
	}

	// The Ids parsed by linuxproc point into the /proc/stat text; the sample
	// must hold copies so that the text can be freed.
	if unsafe.StringData(sample.allId) == unsafe.StringData(stat.CPUStatAll.Id) {
		t.Error("allId shares memory with the parsed /proc/stat text")
	}
	for i := range stat.CPUStats {
		if unsafe.StringData(sample.cpuIds[i]) == unsafe.StringData(stat.CPUStats[i].Id) {
			t.Errorf("cpuIds[%d] shares memory with the parsed /proc/stat text", i)
		}
	}

	// Unchanged Ids are shared with the previous sample instead of copied again.
	next := newCpuSample(readTestProcStat(t, testProcStat), sample)
	if unsafe.StringData(next.allId) != unsafe.StringData(sample.allId) || &next.cpuIds[0] != &sample.cpuIds[0] {
		t.Error("unchanged Ids are not shared with the previous sample")
	}

	// A different set of cpus gets its own Ids.
	changed := newCpuSample(readTestProcStat(t, "cpu  1 2 3 4 5 6 7 8 0 0\ncpu0 1 2 3 4 5 6 7 8 0 0\ncpu2 1 2 3 4 5 6 7 8 0 0\n"), next)
	if !reflect.DeepEqual(changed.cpuIds, []string{"cpu0", "cpu2"}) || &changed.cpuIds[0] == &next.cpuIds[0] {
		t.Errorf("cpuIds = %q after the cpu set changed", changed.cpuIds)
	}

	if newCpuSample(nil, sample) != nil {
		t.Error("newCpuSample(nil) is not nil")
	}
}

func TestGetCpuUtilPercents(t *testing.T) {
	last := cpuTicks{total: 1000, idle: 800}
	if got := getCpuUtilPercents(cpuTicks{total: 1200, idle: 950}, last); got != 25 {
		t.Errorf("getCpuUtilPercents = %d, want 25", got)
	}
	if got := getCpuUtilPercents(last, last); got != 0 {
		t.Errorf("getCpuUtilPercents with no change = %d, want 0", got)
	}
}
