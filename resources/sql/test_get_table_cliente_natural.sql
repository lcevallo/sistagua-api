CALL lc_sp_get_table_cliente_natural(
    1,
    @json_cliente,
    @json_direcciones,
    @json_parentesco
);
SELECT @json_cliente,@json_direcciones,@json_parentesco;