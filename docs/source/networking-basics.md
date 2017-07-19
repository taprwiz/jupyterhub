# Networking basics

## Configuring the Proxy's IP address and port
The Proxy's main IP address setting determines where JupyterHub is available to users.
By default, JupyterHub is configured to be available on all network interfaces
(`''`) on port 8000. **Note**: Use of `'*'` is discouraged for IP configuration;
instead, use of `'0.0.0.0'` is preferred.

Changing the IP address and port can be done with the following command line
arguments:

```bash
jupyterhub --ip=192.168.1.2 --port=443
```

Or by placing the following lines in a configuration file:

```python
c.JupyterHub.ip = '192.168.1.2'
c.JupyterHub.port = 443
```

Port 443 is used as an example since 443 is the default port for SSL/HTTPS.

Configuring only the main IP and port of JupyterHub should be sufficient for most deployments of JupyterHub.
However, more customized scenarios may need additional networking details to
be configured.


## Configuring the Proxy's REST API communication IP address and port (optional)
The Hub service talks to the proxy via a REST API on a secondary port,
whose network interface and port can be configured separately.
By default, this REST API listens on port 8081 of localhost only.

If running the Proxy separate from the Hub,
configure the REST API communication IP address and port with:

```python
# ideally a private network address
c.JupyterHub.proxy_api_ip = '10.0.1.4'
c.JupyterHub.proxy_api_port = 5432
```

## Configuring the Hub if Spawners or Proxy are remote or isolated in containers
The Hub service also listens only on localhost (port 8080) by default.
The Hub needs needs to be accessible from both the proxy and all Spawners.
When spawning local servers, an IP address setting of localhost is fine.
If *either* the Proxy *or* (more likely) the Spawners will be remote or
isolated in containers, the Hub must listen on an IP that is accessible.

```python
c.JupyterHub.hub_ip = '10.0.1.4'
c.JupyterHub.hub_port = 54321
```
