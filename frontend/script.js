/* ─── MAPA ───────────────────────────────────────────────── */
const map = L.map('map', { zoomControl: true }).setView([-23.55052, -46.633308], 12)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19
}).addTo(map)

// Centraliza no usuário ao abrir
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        ({ coords }) => map.setView([coords.latitude, coords.longitude], 15),
        () => console.warn('Geolocalização não disponível.')
    )
}

/* ─── UTILITÁRIOS ────────────────────────────────────────── */
const $ = id => document.getElementById(id)

function showToast(message, type = 'success') {
    const toast = $('toast')
    toast.textContent = message
    toast.className = `toast ${type} show`
    setTimeout(() => { toast.className = 'toast' }, 4000)
}

function setLoading(active) {
    const btn = $('submitBtn')
    const text = btn.querySelector('.btn-text')
    btn.disabled = active
    text.textContent = active ? 'Enviando…' : 'Enviar denúncia'
}

/* ─── NOME DO ARQUIVO SELECIONADO ────────────────────────── */
$('image').addEventListener('change', () => {
    const file = $('image').files[0]
    $('fileText').textContent = file ? file.name : 'Selecionar arquivo…'
})

/* ─── FORMULÁRIO ─────────────────────────────────────────── */
$('reportForm').addEventListener('submit', async (e) => {
    e.preventDefault()

    // Validação manual básica
    const title       = $('title').value.trim()
    const description = $('description').value.trim()
    const category    = $('category').value

    if (!title || !description || !category) {
        showToast('Preencha todos os campos obrigatórios.', 'error')
        return
    }

    if (!navigator.geolocation) {
        showToast('Seu navegador não suporta geolocalização.', 'error')
        return
    }

    setLoading(true)

    navigator.geolocation.getCurrentPosition(
        async ({ coords }) => {
            const formData = new FormData()
            formData.append('title',       title)
            formData.append('description', description)
            formData.append('category',    category)
            formData.append('latitude',    coords.latitude)
            formData.append('longitude',   coords.longitude)

            const image = $('image').files[0]
            if (image) formData.append('image', image)

            try {
                const response = await fetch('http://127.0.0.1:8000/reports', {
                    method: 'POST',
                    body: formData
                })

                if (!response.ok) {
                    throw new Error(`Erro ${response.status}: ${response.statusText}`)
                }

                // Adiciona marcador no mapa
                L.marker([coords.latitude, coords.longitude])
                    .addTo(map)
                    .bindPopup(`<strong>${title}</strong><br>${category}`)
                    .openPopup()

                // Reseta formulário
                $('reportForm').reset()
                $('fileText').textContent = 'Selecionar arquivo…'

                showToast('✓ Denúncia enviada com sucesso!', 'success')

            } catch (err) {
                console.error(err)
                showToast('Erro ao enviar. Verifique se o servidor está ativo.', 'error')
            } finally {
                setLoading(false)
            }
        },
        (err) => {
            console.error(err)
            showToast('Não foi possível obter sua localização.', 'error')
            setLoading(false)
        },
        { timeout: 10000 }
    )
})