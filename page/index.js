const API_BASE = "http://localhost:8000"
const ENDPOINT_CURRENT = `${API_BASE}/obter-leitura`
const ENDPOINT_HISTORY = `${API_BASE}/historico`

const { createApp } = Vue

createApp({
    data() {
        return {
            activeTab: 'current',
            sensors: [],
            history: []
        }
    },
    methods: {
        async fetchSensors() {
            try {
                const { data } = await axios.get(ENDPOINT_HISTORY) // get full history
                const sensors = []

                // create a map of latest value per sensor
                const latestBySensor = {}
                data.forEach(record => {
                    const id = record.id_sensor
                    if (!latestBySensor[id] || new Date(record.data_hora) > new Date(latestBySensor[id].data_hora)) {
                        latestBySensor[id] = record
                    }
                })

                // create grid of 20 sensors P1..P20
                for (let i = 1; i <= 20; i++) {
                    const id = `P${i}`
                    if (latestBySensor[id]) {
                        sensors.push({
                            id_sensor: id,
                            valor: latestBySensor[id].valor,
                            tempo_ocupado: null // optional, can calculate if you want
                        })
                    } else {
                        sensors.push({
                            id_sensor: id,
                            valor: null,
                            tempo_ocupado: 'Não instalado'
                        })
                    }
                }

                this.sensors = sensors
            } catch (error) {
                console.error('Error fetching sensors:', error)
                this.sensors = []
            }
        },
        async fetchHistory() {
            try {
                const { data } = await axios.get(ENDPOINT_HISTORY)
                this.history = data
            } catch (error) {
                console.error('Error fetching history:', error)
            }
        }
    },
    mounted() {
        this.fetchSensors()
        this.fetchHistory()
        setInterval(this.fetchSensors, 200)
        setInterval(this.fetchHistory, 200)
    }
}).mount('#app')
