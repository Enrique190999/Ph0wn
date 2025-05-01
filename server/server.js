const express = require('express')
const app = express();
const PORT = 8099
const cors = require('cors')
app.listen(PORT, () => console.log(`Servidor en marcha en el puerto:${PORT}`))

app.use(express.json())
app.use(cors())
app.post("/",(req,res) => {
    const {username,password} = req.body
    console.log(`USER: ${username} PASSWORD:${password}`)
    res.send("OK")
})