//收盘价涨跌幅背景色处理
function cellStyler(value,row,index){
    if (value == null){
        return '';
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
    if (value == null){
        return '';
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
    if (value == null){
        return '';
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
    if (chg == null){
        return '';
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
    if (value == null){
        return '';
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
    if (chg == null){
        return '';
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
    if (chg == null){
        return '';
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
    if (chg == null){
        return '';
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
    if (chg == null){
        return '';
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
    if (value == null){
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
    if (value == null){
        return '';
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
    if (val == null){
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
    $("#inflection_security_code").val(obj.value);
    inflection_point_grid_query();
    $("#show_stock_info").html("【"+obj.value + " " + obj.name +"】");
    //security_name = obj.name
}
//拐点数据框查询公用方法
function inflection_point_grid_query(){
    var currentDate = new Date();
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var seconds = currentDate.getSeconds();
    if(interval_codes_reload && hours >= 15 && minutes >= 0 && seconds >= 0){
        console.log('非交易时间点，不做更新');
        window.clearInterval(interval_codes_reload);
    }
    var security_code = $("#inflection_security_code").val();
    var size = $("#inflection_size").val();
    if(security_code == '' || security_code == undefined){
        $.messager.show({
            title:'<strong style="color: red;">没有选择股票额</strong>',
            msg:'<strong style="color: red;">so，赶紧选择一只股票吧</strong>',
            showType:'show'
        });
        return;
    }
    $("#inflection_point_grid").datagrid({
        queryParams: {
            security_code: security_code,
            size: size
        }
    });
    $("#interval_time").html(new Date().toLocaleString());
//    get_stock_history_kline(security_code, size);
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

function formatToButton(val,row){
    return '<button type="button" onclick="inflection_security_click(this)" class="easyui-linkbutton" value="'+row.security_code+'" title="'+row.security_name+'" name="'+row.security_name+'">'+row.security_code+'</button>'
}

function change_bgcolor(type){
    var bgcolor = '';
    if(type == 'sell'){
        bgcolor = 'LightGreen';
    }
    else if(type == 'buy'){
        bgcolor = 'Tomato';
    }
    else if(type == 'cancel'){
        bgcolor = '';
    }
    var rows = $('#inflection_point_grid').datagrid('getSelections');
    if(rows.length > 0){
        var index = $('#inflection_point_grid').datagrid('getRowIndex', rows[0])
        var div = $("#inflection_point_data");
        var tr = $($(div).find('div.datagrid-view2').find('.datagrid-row')[index]).css("background-color", bgcolor);
    }

}

function delete_rows(){
    var rows = $('#inflection_point_grid').datagrid('getSelections');
    if(rows.length > 0){
        var i = 0;
        var index = -1;
        for(i; i < rows.length; i++){
            index = $('#inflection_point_grid').datagrid('getRowIndex', rows[i]);
            $('#inflection_point_grid').datagrid('deleteRow', index);
        }
    }
}

function formatDayKlineId(val, row){
    return 'day_kline_' + val;
}

function get_stock_history_kline(security_code, size){
    if(security_code != '' && security_code != undefined){
        $.ajax({
            url: '/history_kline_get?security_code=' + security_code + '&size=' + size,
            type: 'get',
            data: {},
            dataType: 'json',
            success: function(data){
                analysis_history_kline(data);
            }
        });
    }
}


function splitData(rawData) {
    var categoryData = [];
    var values = [];
    var volumns = [];
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i]);
        volumns.push(rawData[i][4]);
    }
    return {
        categoryData: categoryData,
        values: values,
        volumns: volumns
    };
}

function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data.values[i - j][1];
        }
        result.push(+(sum / dayCount).toFixed(3));
    }
    return result;
}

function analysis_history_kline(rawData) {
    var security_code = $("#show_stock_info").html();
    var myChart = echarts.init(document.getElementById('main'), 'shine');
    var data = splitData(rawData);

    myChart.setOption(option = {
        backgroundColor: '#eee',
        animation: false,
        legend: {
            bottom: 10,
            left: 'center',
            data: [security_code, 'MA5', 'MA10', 'MA20', 'MA30']
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            },
            backgroundColor: 'rgba(245, 245, 245, 0.8)',
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
                color: '#000'
            },
            position: function (pos, params, el, elRect, size) {
                var obj = {top: 10};
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            },
            extraCssText: 'width: 170px'
        },
        axisPointer: {
            link: {xAxisIndex: 'all'},
            label: {
                backgroundColor: '#777'
            }
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: false
                },
                brush: {
                    type: ['lineX', 'clear']
                }
            }
        },
        brush: {
            xAxisIndex: 'all',
            brushLink: 'all',
            outOfBrush: {
                colorAlpha: 0.1
            }
        },
        grid: [
            {
                left: '2%',
                right: '2%',
                height: '62%'
            },
            {
                left: '2%',
                right: '2%',
                top: '68%',
                height: '16%'
            }
        ],
        xAxis: [
            {
                type: 'category',
                data: data.categoryData,
                scale: true,
                boundaryGap : false,
                axisLine: {onZero: false},
                splitLine: {show: true},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    z: 100
                }
            },
            {
                type: 'category',
                gridIndex: 1,
                data: data.categoryData,
                scale: true,
                boundaryGap : false,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: true},
                axisLabel: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    label: {
                        formatter: function (params) {
                            var seriesValue = (params.seriesData[0] || {}).value;
                            return params.value
                            + (seriesValue != null
                                ? '\n' + echarts.format.addCommas(seriesValue)
                                : ''
                            );
                        }
                    }
                }
            }
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: true},
                axisTick: {show: false},
                splitLine: {show: true}
            }
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 97,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                top: '85%',
                start: 98,
                end: 100
            }
        ],
        series: [
            {
                name: security_code,
                type: 'candlestick',
                data: data.values,
                itemStyle: {
                    normal: {
                        borderColor: null,
                        borderColor0: null
                    }
                },
                tooltip: {
                    formatter: function (param) {
                        param = param[0];
                        return [
                            '时间: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                            '开: ' + param.data[0] + '<br/>',
                            '收: ' + param.data[1] + '<br/>',
                            '低: ' + param.data[2] + '<br/>',
                            '高: ' + param.data[3] + '<br/>'
                        ].join('');
                    }
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: calculateMA(5, data),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: calculateMA(10, data),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: calculateMA(20, data),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: calculateMA(30, data),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'Volumn',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data.volumns
            }
        ]
    }, true);

    // myChart.on('brushSelected', renderBrushed);

    // function renderBrushed(params) {
    //     var sum = 0;
    //     var min = Infinity;
    //     var max = -Infinity;
    //     var countBySeries = [];
    //     var brushComponent = params.brushComponents[0];

    //     var rawIndices = brushComponent.series[0].rawIndices;
    //     for (var i = 0; i < rawIndices.length; i++) {
    //         var val = data.values[rawIndices[i]][1];
    //         sum += val;
    //         min = Math.min(val, min);
    //         max = Math.max(val, max);
    //     }

    //     panel.innerHTML = [
    //         '<h3>STATISTICS:</h3>',
    //         'SUM of open: ' + (sum / rawIndices.length).toFixed(4) + '<br>',
    //         'MIN of open: ' + min.toFixed(4) + '<br>',
    //         'MAX of open: ' + max.toFixed(4) + '<br>'
    //     ].join(' ');
    // }

//    myChart.dispatchAction({
//        type: 'brush',
//        areas: [
//            {
//                brushType: 'lineX',
//                coordRange: ['2015-06-02', '2016-06-20'],
//                xAxisIndex: 0
//            }
//        ]
//    });
}

function simulated_short_line_stock(){
    var rows = $('#simulated_stocks').datagrid('getSelections');
    if(rows.length == 0){
        $.messager.alert('警告', '请先选择一个股票', 'warning');
        return;
    }
    $("#simulated_form").form('submit', {
        url: 'simulated_short_line_stock_post',
        dataType: 'json',
        success: function(data){
            $("#simulated_short_line_stock_grid").datagrid({
                data: $.parseJSON(data)['rows']
            });
        }
    });
}

function cellRelateEarningsDiffMoney(value,row,index){
    var diff_earnings = row['diff_earnings'];
    if(diff_earnings > 0){
        return 'background-color:red; color:gold;';
    }
    else if(diff_earnings < 0){
        return 'background-color:green; color:gold;';
    }
}

function myformatter(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    return y+'-'+(m<10?('0'+m):m)+'-'+(d<10?('0'+d):d);
}
function myparser(s){
    if (!s) return new Date();
    var ss = (s.split('-'));
    var y = parseInt(ss[0],10);
    var m = parseInt(ss[1],10);
    var d = parseInt(ss[2],10);
    if (!isNaN(y) && !isNaN(m) && !isNaN(d)){
        return new Date(y,m-1,d);
    } else {
        return new Date();
    }
}

function formatSimulatedDirection(val,row){
    if (val == 'buy'){
        return '买'
    }
    else{
        return '卖';
    }
}

function simulatedStockClick(index, rowData){
    security_code = rowData.security_code
    security_name = rowData.security_name
    $("#simulated_security_code").val(security_code);
    $("#simulated_stock_info").html("【" + security_code + " " + security_name + "】");
    $("#simulated_short_line_stock_grid").datagrid({data: []});
}

function cellEarningsDiffStyler(value,row,index){
    if (value == ''){
        return '';
    }
    else if (value > 0){
        return 'background-color:red; color:gold;';
    }
    else if(value < 0){
        return 'background-color:green; color:gold;';
    }
}