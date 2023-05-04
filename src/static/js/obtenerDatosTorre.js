
function obtenerDatosApartamento(id){
    formulario = document.getElementById('formulario')
    btn = document.getElementById('btn')
    
    tabla_torre = document.getElementById(`tabla_torre${id}`)
    tabla_foto_servicio_publico = document.getElementById(`tabla_foto_servicio_publico${id}`)
    tabla_servicio_publico = document.getElementById(`tabla_servicio_publico${id}`)
    tabla_consumo = document.getElementById(`tabla_consumo${id}`)
    tabla_valor = document.getElementById(`tabla_valor${id}`)
    tabla_fecha_corte = document.getElementById(`tabla_fecha_corte${id}`)
    tabla_fecha_recibo = document.getElementById(`tabla_fecha_recibo${id}`)

    torre = document.getElementById(`torre`)
    foto_servicio_publico = document.getElementById(`foto_servicio_publico`)
    servicio_publico = document.getElementById(`servicio_publico`)
    consumo = document.getElementById(`consumo`)
    valor = document.getElementById(`valor`)
    fecha_corte = document.getElementById(`fecha_corte`)
    fecha_recibo = document.getElementById(`fecha_recibo`)

    torre.value = tabla_torre.innerHTML
    foto_servicio_publico.value = tabla_foto_servicio_publico.innerHTML
    servicio_publico.value = tabla_servicio_publico.innerHTML
    consumo.value = tabla_consumo.innerHTML
    valor.value = tabla_valor.innerHTML
    fecha_corte.value = tabla_fecha_corte.innerHTML
    fecha_recibo.value = tabla_fecha_recibo.innerHTML

    formulario.action = `/editar_torre/${id}`
    // btn.innerHTML = 'Actualizar'
}