package install

const kibanaConfigYml = `  
server.name: kibana
server.host: "0"

elasticsearch.hosts: [ "http://elasticsearch:9200" ]
elasticsearch.username: elastic
elasticsearch.password: changeme
xpack.monitoring.ui.container.elasticsearch.enabled: true

xpack.ingestManager.enabled: true
xpack.ingestManager.registryUrl: "http://package-registry:8080"
xpack.ingestManager.fleet.enabled: true
xpack.ingestManager.fleet.elasticsearch.host: "http://localhost:9200"
xpack.ingestManager.fleet.kibana.host: "http://localhost:5601"
xpack.ingestManager.fleet.tlsCheckDisabled: true

xpack.encryptedSavedObjects.encryptionKey: "12345678901234567890123456789012"
`
