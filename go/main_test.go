package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// do sends a request to a fresh mux and returns the recorded response.
func do(method, path string) *httptest.ResponseRecorder {
	req := httptest.NewRequest(method, path, nil)
	w := httptest.NewRecorder()
	newMux().ServeHTTP(w, req)
	return w
}

func parseJSON(t *testing.T, w *httptest.ResponseRecorder) map[string]any {
	t.Helper()
	var m map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &m); err != nil {
		t.Fatalf("invalid JSON body: %v\nbody: %s", err, w.Body.String())
	}
	return m
}

// ── GET / ────────────────────────────────────────────────────────────────────

func TestRootStatus200(t *testing.T) {
	if got := do(http.MethodGet, "/").Code; got != http.StatusOK {
		t.Errorf("got %d, want 200", got)
	}
}

func TestRootContentType(t *testing.T) {
	ct := do(http.MethodGet, "/").Header().Get("Content-Type")
	if !strings.Contains(ct, "application/json") {
		t.Errorf("Content-Type=%q, want application/json", ct)
	}
}

func TestRootValidJSON(t *testing.T) {
	w := do(http.MethodGet, "/")
	var v any
	if err := json.Unmarshal(w.Body.Bytes(), &v); err != nil {
		t.Errorf("invalid JSON: %v", err)
	}
}

func TestRootHasServiceField(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/"))
	if _, ok := m["service"]; !ok {
		t.Error("missing field: service")
	}
}

func TestRootHasVersionField(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/"))
	if _, ok := m["version"]; !ok {
		t.Error("missing field: version")
	}
}

func TestRootHasRoutesField(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/"))
	if _, ok := m["routes"]; !ok {
		t.Error("missing field: routes")
	}
}

func TestRootServiceValue(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/"))
	if m["service"] != "go-info" {
		t.Errorf("service=%q, want go-info", m["service"])
	}
}

func TestRootVersionValue(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/"))
	if m["version"] != "1.0.0" {
		t.Errorf("version=%q, want 1.0.0", m["version"])
	}
}

func TestRootRoutesIsNonEmptyArray(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/"))
	routes, ok := m["routes"].([]any)
	if !ok || len(routes) == 0 {
		t.Error("routes should be a non-empty JSON array")
	}
}

// ── GET /health ───────────────────────────────────────────────────────────────

func TestHealthStatus200(t *testing.T) {
	if got := do(http.MethodGet, "/health").Code; got != http.StatusOK {
		t.Errorf("got %d, want 200", got)
	}
}

func TestHealthContentType(t *testing.T) {
	ct := do(http.MethodGet, "/health").Header().Get("Content-Type")
	if !strings.Contains(ct, "application/json") {
		t.Errorf("Content-Type=%q, want application/json", ct)
	}
}

func TestHealthValidJSON(t *testing.T) {
	w := do(http.MethodGet, "/health")
	var v any
	if err := json.Unmarshal(w.Body.Bytes(), &v); err != nil {
		t.Errorf("invalid JSON: %v", err)
	}
}

func TestHealthHasStatusField(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/health"))
	if _, ok := m["status"]; !ok {
		t.Error("missing field: status")
	}
}

func TestHealthHasTimestampField(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/health"))
	if _, ok := m["timestamp"]; !ok {
		t.Error("missing field: timestamp")
	}
}

func TestHealthStatusOK(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/health"))
	if m["status"] != "ok" {
		t.Errorf("status=%q, want ok", m["status"])
	}
}

func TestHealthTimestampIsRFC3339(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/health"))
	ts, ok := m["timestamp"].(string)
	if !ok {
		t.Fatal("timestamp is not a string")
	}
	if _, err := time.Parse(time.RFC3339, ts); err != nil {
		t.Errorf("timestamp %q is not RFC3339: %v", ts, err)
	}
}

// ── GET /info ─────────────────────────────────────────────────────────────────

func TestInfoStatus200(t *testing.T) {
	if got := do(http.MethodGet, "/info").Code; got != http.StatusOK {
		t.Errorf("got %d, want 200", got)
	}
}

func TestInfoContentType(t *testing.T) {
	ct := do(http.MethodGet, "/info").Header().Get("Content-Type")
	if !strings.Contains(ct, "application/json") {
		t.Errorf("Content-Type=%q, want application/json", ct)
	}
}

func TestInfoValidJSON(t *testing.T) {
	w := do(http.MethodGet, "/info")
	var v any
	if err := json.Unmarshal(w.Body.Bytes(), &v); err != nil {
		t.Errorf("invalid JSON: %v", err)
	}
}

func TestInfoHasHostname(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if _, ok := m["hostname"]; !ok {
		t.Error("missing field: hostname")
	}
}

func TestInfoHasGoVersion(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if _, ok := m["go_version"]; !ok {
		t.Error("missing field: go_version")
	}
}

func TestInfoHasOS(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if _, ok := m["os"]; !ok {
		t.Error("missing field: os")
	}
}

func TestInfoHasArch(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if _, ok := m["arch"]; !ok {
		t.Error("missing field: arch")
	}
}

func TestInfoHasNumCPU(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if _, ok := m["num_cpu"]; !ok {
		t.Error("missing field: num_cpu")
	}
}

func TestInfoNumCPUPositive(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	cpu, ok := m["num_cpu"].(float64)
	if !ok || cpu <= 0 {
		t.Errorf("num_cpu=%v, want > 0", m["num_cpu"])
	}
}

func TestInfoGoVersionNotEmpty(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if v, _ := m["go_version"].(string); v == "" {
		t.Error("go_version should not be empty")
	}
}

func TestInfoOSNotEmpty(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if v, _ := m["os"].(string); v == "" {
		t.Error("os should not be empty")
	}
}

func TestInfoArchNotEmpty(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/info"))
	if v, _ := m["arch"].(string); v == "" {
		t.Error("arch should not be empty")
	}
}

// ── GET /metrics ──────────────────────────────────────────────────────────────

func TestMetricsStatus200(t *testing.T) {
	if got := do(http.MethodGet, "/metrics").Code; got != http.StatusOK {
		t.Errorf("got %d, want 200", got)
	}
}

func TestMetricsContentType(t *testing.T) {
	ct := do(http.MethodGet, "/metrics").Header().Get("Content-Type")
	if !strings.Contains(ct, "application/json") {
		t.Errorf("Content-Type=%q, want application/json", ct)
	}
}

func TestMetricsValidJSON(t *testing.T) {
	w := do(http.MethodGet, "/metrics")
	var v any
	if err := json.Unmarshal(w.Body.Bytes(), &v); err != nil {
		t.Errorf("invalid JSON: %v", err)
	}
}

func TestMetricsHasUptimeSeconds(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	if _, ok := m["uptime_seconds"]; !ok {
		t.Error("missing field: uptime_seconds")
	}
}

func TestMetricsHasGoroutines(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	if _, ok := m["goroutines"]; !ok {
		t.Error("missing field: goroutines")
	}
}

func TestMetricsHasAllocMB(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	if _, ok := m["alloc_mb"]; !ok {
		t.Error("missing field: alloc_mb")
	}
}

func TestMetricsHasSysMB(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	if _, ok := m["sys_mb"]; !ok {
		t.Error("missing field: sys_mb")
	}
}

func TestMetricsGoroutinesPositive(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	g, ok := m["goroutines"].(float64)
	if !ok || g <= 0 {
		t.Errorf("goroutines=%v, want > 0", m["goroutines"])
	}
}

func TestMetricsUptimeNonNegative(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	u, ok := m["uptime_seconds"].(float64)
	if !ok || u < 0 {
		t.Errorf("uptime_seconds=%v, want >= 0", m["uptime_seconds"])
	}
}

func TestMetricsAllocMBNonNegative(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	a, ok := m["alloc_mb"].(float64)
	if !ok || a < 0 {
		t.Errorf("alloc_mb=%v, want >= 0", m["alloc_mb"])
	}
}

func TestMetricsSysMBPositive(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/metrics"))
	s, ok := m["sys_mb"].(float64)
	if !ok || s <= 0 {
		t.Errorf("sys_mb=%v, want > 0", m["sys_mb"])
	}
}

// ── 405 Method Not Allowed ────────────────────────────────────────────────────

func TestPostRootReturns405(t *testing.T) {
	if got := do(http.MethodPost, "/").Code; got != http.StatusMethodNotAllowed {
		t.Errorf("got %d, want 405", got)
	}
}

func TestPostHealthReturns405(t *testing.T) {
	if got := do(http.MethodPost, "/health").Code; got != http.StatusMethodNotAllowed {
		t.Errorf("got %d, want 405", got)
	}
}

func TestPostInfoReturns405(t *testing.T) {
	if got := do(http.MethodPost, "/info").Code; got != http.StatusMethodNotAllowed {
		t.Errorf("got %d, want 405", got)
	}
}

func TestPostMetricsReturns405(t *testing.T) {
	if got := do(http.MethodPost, "/metrics").Code; got != http.StatusMethodNotAllowed {
		t.Errorf("got %d, want 405", got)
	}
}

func TestPutHealthReturns405(t *testing.T) {
	if got := do(http.MethodPut, "/health").Code; got != http.StatusMethodNotAllowed {
		t.Errorf("got %d, want 405", got)
	}
}

func TestDeleteHealthReturns405(t *testing.T) {
	if got := do(http.MethodDelete, "/health").Code; got != http.StatusMethodNotAllowed {
		t.Errorf("got %d, want 405", got)
	}
}

func TestMethodNotAllowedContentType(t *testing.T) {
	ct := do(http.MethodPost, "/health").Header().Get("Content-Type")
	if !strings.Contains(ct, "application/json") {
		t.Errorf("Content-Type=%q, want application/json", ct)
	}
}

func TestMethodNotAllowedValidJSON(t *testing.T) {
	w := do(http.MethodPost, "/info")
	var v any
	if err := json.Unmarshal(w.Body.Bytes(), &v); err != nil {
		t.Errorf("invalid JSON on 405 response: %v", err)
	}
}

// ── 404 Not Found ─────────────────────────────────────────────────────────────

func TestNonexistentPath404(t *testing.T) {
	if got := do(http.MethodGet, "/nonexistent").Code; got != http.StatusNotFound {
		t.Errorf("got %d, want 404", got)
	}
}

func TestUnknownNestedPath404(t *testing.T) {
	if got := do(http.MethodGet, "/unknown/path").Code; got != http.StatusNotFound {
		t.Errorf("got %d, want 404", got)
	}
}

func TestNotFoundContentType(t *testing.T) {
	ct := do(http.MethodGet, "/nonexistent").Header().Get("Content-Type")
	if !strings.Contains(ct, "application/json") {
		t.Errorf("Content-Type=%q, want application/json", ct)
	}
}

func TestNotFoundValidJSON(t *testing.T) {
	w := do(http.MethodGet, "/nonexistent")
	var v any
	if err := json.Unmarshal(w.Body.Bytes(), &v); err != nil {
		t.Errorf("invalid JSON on 404 response: %v", err)
	}
}

func TestNotFoundHasErrorField(t *testing.T) {
	m := parseJSON(t, do(http.MethodGet, "/nonexistent"))
	if _, ok := m["error"]; !ok {
		t.Error("404 response missing field: error")
	}
}
