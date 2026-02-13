def test_dashboard_route_mounts():
    import dashboard

    routes = {route.path for route in dashboard.app.routes}
    assert "/api/marketing/playbooks" in routes
    assert "/api/templates" in routes
    assert "/api/accounts" in routes
    assert "/api/accounts/generate-qr" in routes
    assert "/api/accounts/add-session" in routes
    assert "/api/accounts/send-code" in routes
    assert "/api/proxies" in routes
    assert "/api/proxies/test" in routes
    assert "/api/health/report" in routes
    assert "/api/stats/summary" in routes
    assert "/api/logs" in routes
    assert "/api/schedules" in routes
    assert "/api/batch/send-message" in routes
    assert "/api/workspace/accounts" in routes
    assert "/api/workspace/accounts/generate-qr" in routes
    assert "/api/workspace/proxies" in routes
    assert "/api/workspace/health/report" in routes
    assert "/api/workspace/schedules" in routes
