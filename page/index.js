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
                const { data } = await axios.get(`${API_BASE}/sensores/json`)
                this.sensors = data.sensors.map(sensor => {
                    // normalize value
                    let valor = sensor.valor
                    if (typeof valor === "string") {
                        valor = valor.toLowerCase()
                        if (/ocupad[oa]/.test(valor)) valor = "Ocupado"
                        else if (/livre/.test(valor)) valor = "Livre"
                    }
                    return { ...sensor, valor }
                })
            } catch (error) {
                console.error('Error fetching sensors:', error)
                this.sensors = []
            }
        },
        async fetchHistory() {
            try {
                const { data } = await axios.get(ENDPOINT_HISTORY)
                this.history = data.map(h => {
                    let valor = h.valor
                    if (typeof valor === "string") {
                        valor = valor.toLowerCase()
                        if (/ocupad[oa]/.test(valor)) valor = "Ocupado"
                        else if (/livre/.test(valor)) valor = "Livre"
                    }
                    return { ...h, valor }
                })
            } catch (error) {
                console.error('Error fetching history:', error)
            }
        }
    },
    mounted() {
        this.fetchSensors()
        this.fetchHistory()
        const ws = new WebSocket("ws://localhost:8000/ws")

        ws.onopen = () => console.log("Connected to WebSocket")

        ws.onmessage = (event) => {
            console.log("Leitura broadcasted:", event.data)

            let payload
            try {
                payload = JSON.parse(event.data)
            } catch {
                console.error("Invalid WebSocket message:", event.data)
                return
            }

            const index = this.sensors.findIndex(s => s.id_sensor === payload.id_sensor)
            if (index !== -1) {
                let valor = payload.valor.toLowerCase()
                if (/ocupad/.test(valor)) valor = "Ocupado"
                else if (/livre/.test(valor)) valor = "Livre"
                else valor = payload.valor

                this.sensors[index] = { ...this.sensors[index], valor }
            }
        }

        ws.onclose = () => console.log("WebSocket disconnected")
        ws.onerror = (err) => console.error("WebSocket error:", err)
    }
}).mount('#app')
