
### Generar ppc para la tabla renta variable

En el momento en que se carga una transaccion disparar un evento que modifique la tabla renta variable (Cruzando datos con el ticket). 

## Tabla renta variable (o rendimiento dinamico)
### Calculo PPC
- Para las transacciones de compra:

	`(Precio unitario de compra * Cantidad transaccion + PPC * cantidad en renta variable) / (cant transaccion + cant renta)`

- Para venta: 
	La venta no influye en el precio promedio de compra, solamente la cantidad

### Calculo de fecha ponderada
`(Fecha transaccion * Cantidad transaccion + Fecha ponderada * cantidad en renta variable) / (cant transaccion + cant renta)`
