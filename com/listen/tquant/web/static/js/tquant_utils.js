function tquant_ajax(type, url, data, success, dataType, appendId) {
    console.log(appendId)
    $.ajax({
        url: url,
        type: type,
        data: data,
        dataType: dataType,
        success: function(data){
            console.log('data:' + data)
            $('#' + appendId).append(data);
            if (success instanceof Function){
                success(data);
            }
        }
    });
}