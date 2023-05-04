
function obtenerDatos(id){
    formulario = document.getElementById('formulario')
    btn = document.getElementById('btn')
    
    tabla_torre = document.getElementById(`tabla_torre${id}`)
    tabla_apartamento = document.getElementById(`tabla_apartamento${id}`)
    tabla_servicio_publico = document.getElementById(`tabla_servicio_publico${id}`)
    tabla_consumo = document.getElementById(`tabla_consumo${id}`)
    tabla_valor = document.getElementById(`tabla_valor${id}`)
    tabla_fecha_corte = document.getElementById(`tabla_fecha_corte${id}`)
    tabla_fecha_recibo = document.getElementById(`tabla_fecha_recibo${id}`)

    torre = document.getElementById(`torre`)
    apartamento = document.getElementById(`apartamento`)
    servicio_publico = document.getElementById(`servicio_publico`)
    consumo = document.getElementById(`consumo`)
    valor = document.getElementById(`valor`)
    fecha_corte = document.getElementById(`fecha_corte`)
    fecha_recibo = document.getElementById(`fecha_recibo`)

    torre.value = tabla_torre.innerHTML
    apartamento.value = tabla_apartamento.innerHTML
    servicio_publico.value = tabla_servicio_publico.innerHTML
    consumo.value = tabla_consumo.innerHTML
    valor.value = tabla_valor.innerHTML
    fecha_corte.value = tabla_fecha_corte.innerHTML
    fecha_recibo.value = tabla_fecha_recibo.innerHTML

    formulario.action = `/editar_apartamento/${id}`
    // btn.innerHTML = 'Actualizar'
}