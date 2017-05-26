//收盘价涨跌幅背景色处理
function cellStyler(value,row,index){
    if (value == '' || value == undefined || value == 'null'){
        return ''
    }
    else if (value >= 3){
        return 'background-color:red; color:gold;';
    }
    else if(value > 0){
        return 'color:red;'
    }
    else if(value <= -3){
        return 'background-color:green; color:gold;';
    }
    else if(value < 0){
        return 'color:green;';
    }
    else {
        return '';
    }
}
//成交量涨跌幅背景色处理
function cellVolStyler(value,row,index){
    if (value == '' || value == undefined || value == 'null'){
        return ''
    }
    else if (value >= 50){
        return 'background-color:red; color:gold;';
    }
    else if(value > 0){
        return 'color:red;'
    }
    else if(value <= -50){
        return 'background-color:green; color:gold;';
    }
    else if(value < 0){
        return 'color:green;';
    }
    else{
        return '';
    }
}
//钱流背景色处理
function cellMoneyFlowStyler(value,row,index){
    if (value == '' || value == undefined || value == 'null'){
        return ''
    }
    else if (value >= 130){
        return 'background-color:red; color:gold;';
    }
    else if(value > 100){
        return 'color:red;'
    }
    else if(value <= 70){
        return 'background-color:green; color:gold;';
    }
    else if(value < 100){
        return 'color:green;';
    }
    else{
        return '';
    }
}
//根据收盘价涨跌幅设置收盘价的背景色
function cellCloseStyler(value,row,index){
    chg = row['close_chg'];
    if (chg == '' || chg == undefined || chg == 'null'){
        return ''
    }
    if (chg >= 3){
        return 'background-color:red; color:gold;';
    }
    else if(chg > 0){
        return 'color: red;';
    }
    else if(chg <= -3){
        return 'background-color:green; color:gold;';
    }
    else if(chg < 0){
        return 'color: green;';
    }
    else{
        return '';
    }
}
//收盘价/开盘价涨跌幅背景色
function cellCloseOpenStyler(value,row,index){
    if (value == '' || value == undefined || value == 'null'){
        return ''
    }
    else if (value >= 3){
        return 'background-color:red; color:gold;';
    }
    else if(value > 0){
        return 'color:red;'
    }
    else if(value <= -3){
        return 'background-color:green; color:gold;';
    }
    else if(value < 0){
        return 'color:green;';
    }
    else{
        return '';
    }
}
//根据日均价涨跌幅设置日均价的背景色
function cellDayAvgPriceStyler(value,row,index){
    chg = row['price_avg_chg'];
    if (chg == '' || chg == undefined || chg == 'null'){
        return ''
    }
    else if (chg >= 3){
        return 'background-color:red; color:gold;';
    }
    else if (chg > 0){
        return 'color:red;';
    }
    else if(chg <= -3){
        return 'background-color:green; color:gold;';
    }
    else if(chg < 0){
        return 'color: green;';
    }
    else{
        return '';
    }
}
//根据3日均价涨跌幅设置3日均价的背景色
function cellDayAvgPrice3Styler(value,row,index){
    chg = row['price_avg_chg_3'];
    if (chg == '' || chg == undefined || chg == 'null'){
        return ''
    }
    else if (chg >= 3){
        return 'background-color:red; color:gold;';
    }
    else if (chg > 0){
        return 'color:red;';
    }
    else if(chg <= -3){
        return 'background-color:green; color:gold;';
    }
    else if(chg < 0){
        return 'color: green;';
    }
    else{
        return '';
    }
}
//根据5日均价涨跌幅设置5日均价的背景色
function cellDayAvgPrice5Styler(value,row,index){
    chg = row['price_avg_chg_5'];
    if (chg == '' || chg == undefined || chg == 'null'){
        return ''
    }
    else if (chg >= 3){
        return 'background-color:red; color:gold;';
    }
    else if (chg > 0){
        return 'color:red;';
    }
    else if(chg <= -3){
        return 'background-color:green; color:gold;';
    }
    else if(chg < 0){
        return 'color: green;';
    }
    else{
        return '';
    }
}
//根据10日均价涨跌幅设置10日均价的背景色
function cellDayAvgPrice10Styler(value,row,index){
    chg = row['price_avg_chg_10'];
    if (chg == '' || chg == undefined || chg == 'null'){
        return ''
    }
    else if (chg >= 3){
        return 'background-color:red; color:gold;';
    }
    else if (chg > 0){
        return 'color:red;';
    }
    else if(chg <= -3){
        return 'background-color:green; color:gold;';
    }
    else if(chg < 0){
        return 'color: green;';
    }
    else{
        return '';
    }
}
//根据10日均价涨跌幅平均值背景色，即1%的规律
function cellPercent1Styler(value, row, index){
    if (value == '' || value == undefined || value == 'null'){
        return ''
    }
    else if(value >= 1){
        return 'background-color:red; color:gold;';
    }
    else if(value > 0){
        return 'color: red;';
    }
    else if(value <= -1){
        return 'background-color:green; color:gold;';
    }
    else if(value < 0){
        return 'color: green;';
    }
}
//(1,3,5,10)日均涨跌幅背景色
function cellDayAvgStyler(value,row,index){
    if (value == '' || value == undefined || value == 'null'){
        return ''
    }
    else if (value >= 1){
        return 'background-color:red; color:gold;';
    }
    else if(value > 0){
        return 'color:red;'
    }
    else if(value <= -1){
        return 'background-color:green; color:gold;';
    }
    else if(value < 0){
        return 'color:green;';
    }
    else{
        return '';
    }
}
//涨跌幅字段值设置百分号
function formatPercent(val,row){
    if (val == null){
        return ''
    }
    else{
        return '' + val+'%';
    }
}
function get_diff_up_down_img(val){
    if (val == '' || val == undefined || val == 'null'){
        return ''
    }
    else if (val >= 1){
        return '../static/img/up1.gif'
    }
    else if(val > 0){
        return '../static/img/up2.gif'
    }
    else if(val == 0){
        return '../static/img/stop2.gif'
    }
    else if(val <= -1){
        return '../static/img/down1.gif'
    }
    else if(val < 0){
        return '../static/img/down2.gif'
    }
}
//箭头方向图片显示
function formatImg(val, row){
    var src = get_diff_up_down_img(val);
    return '<img src="'+src+'"></img>';
}
//拐点分析数据框重新加载
function inflection_point_grid_reload(){
    $('#inflection_point_grid').datagrid('reload');
}
//拐点数据框数分页变动查询
function inflection_changesize(size){
    var security_code = $("#inflection_security_code").val();
    if(security_code == '' || security_code == undefined){
        $.messager.alert('警告', '请先单击一个股票', 'warning');
        return;
    }
    $("#inflection_size").val(size);
    inflection_point_grid_query();
}
//股票代码单击事件，结果是执行拐点数据框查询，并显示本次的股票信息
function inflection_security_click(obj){
    console.log(obj);
    $("#inflection_security_code").val(obj.value);
    inflection_point_grid_query();
    $("#show_stock_info").html("【"+obj.value + " " + obj.name +"】");
}
//拐点数据框查询公用方法
function inflection_point_grid_query(){
    var security_code = $("#inflection_security_code").val();
    var size = $("#inflection_size").val();
    console.log(security_code);
    $("#inflection_point_grid").datagrid({
        queryParams: {
            security_code: security_code,
            size: size
        }
    });
}
//查询全部股票列表
function query_all_stockinfo(){
    var url = '/inflection_point_get';
    $.ajax({
        url: url,
        type: 'get',
        data: {},
        dataType: 'json',
        success: function(data){
            data = data['row'];
            $.each(data, function(i, obj){
                $('#inflection_stock_codes').append('<button type="button" style="width: 70px;" onclick="inflection_security_click(this)" class="easyui-linkbutton" value="'+obj.security_code+'" title="'+obj.security_code+'" name="'+obj.security_name+'">'+obj.security_name+'</button>');
            });
            $.parser.parse($('#inflection_stock_codes'));
            console.log('inflection_stock_codes ' + new Date());
        }
    });
}
