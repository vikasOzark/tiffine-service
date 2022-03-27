
$('#non_veg_id').click(function(){
    let type = "non_veg";
    type_val = { type_val : type };

    $.ajax({
    url : '/filter_menu/' ,
    method : 'GET',
    data : type_val,
    dataType : 'json',
    success : function(data){
        console.log(data.datas)
    }
    })
})
$('#veg_id').click(function(){
    let type = "veg";
    type_val = { type_val : type };

    $.ajax({
    url : '/filter_menu/',
    method : 'GET',
    data : type_val,
    dataType : 'json',
    success : function(data){
        console.log(data.datas)
    }
    })
})
    
       