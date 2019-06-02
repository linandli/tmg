$SERVER = 'http://121.42.160.108:8088';

var addDiv = function(id) {
    $("#chart-show").append('<div class="chart-div" id="{id}"></div>'.replace('{id}', id));
}

function longToDatetimeFormat(longTypeDate) {
    var datetimeType = "";
    var date = new Date();

    date.setTime(longTypeDate);

    datetimeType += date.getHours(date) + ":" + date.getMinutes(date);

    return datetimeType;
} 

var getPlantsFh = function(plantId) {
    $.ajax({
        type: 'GET',
        url: $SERVER + '/plants/?plantid=' + plantId,
        contentType: "application/json; charset=utf-8",
        timeout: 15000
    }).then(function(r) {
        if(r) {
            $("#chart-show").empty()

            $.each(r, function (name, val) {
                var xAxisData = new Array();
                var yAxisData = new Array();
                
                if(val == null) {
                    return true;
                }

                $.each(val, function (k, v) {
                    xAxisData.push(longToDatetimeFormat(k * 1000));
                    yAxisData.push(v);
                });

                addDiv(name);

                var myChart = echarts.init(document.getElementById(name), 'light');
                option = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: [name]
                    },
                    toolbox: {
                        show: false,
                        feature: {
                            mark: { show: true },
                            dataView: { show: true, readOnly: false },
                            magicType: { show: true, type: ['line', 'bar', 'stack', 'tiled'] },
                            restore: { show: true },
                            saveAsImage: { show: true }
                        }
                    },
                    calculable: true,
                    xAxis: [
                        {
                            type: 'category',
                            boundaryGap: false,
                            data: xAxisData
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value'
                        }
                    ],
                    series: [
                        {
                            name: name,
                            type: 'line',
                            stack: '总量',
                            data: yAxisData
                        }
                    ]
                };

                myChart.setOption(option);
            });

            $("#load-title").text("负荷数据");
        }
        else {
            $("#load-title").text("暂无数据");
        }
    });
}

var getPlantList = function() {
    $.ajax({
        type: 'GET',
        url: $SERVER + '/plants/info?plantid=all',
        contentType: "application/json; charset=utf-8",
        timeout: 15000
    }).then(function(res) {
        if(res) {
            $("#plantsList").empty();
            $("#plantsList").append('<option>请选择</option>');

            $.each(res, function (plantId, item) {
                $("#plantsList").append('<option value="{id}">{plant_id} - {name}</option>'.replace('{id}', item[0]).replace('{plant_id}', item[0]).replace('{name}', item[1]));
            });

            $('select').comboSelect();
        }
        else {
            alert("加载电厂失败，请检查网络是否正常！");
        }        
    });
}

var tableTemples = '<table class="table-show"> ' +
    '<thead ><tr><th colspan = "2" > {title} </th> </tr> <tr><th> 指标 </th> <th> 值 </th> </tr> </thead> <tbody>{tbody}</tbody> </table>';


var getPlantElectric = function(plantId) {
    $.ajax({
        type: 'GET',
        url: $SERVER + '/plants/electric?plantid=' + plantId,
        contentType: "application/json; charset=utf-8",
        timeout: 15000
    }).then(function (res) {
        if(res) {
            $("#show-electric").empty();

            $.each(res, function(title, item) {
                var tbTmp = tableTemples;
                tbTmp = tbTmp.replace("{title}", title);
                data = new Array();
                var tbody = "";

                $.each(item, function(k, v) {
                    tbody += "<tr> <td> " + k + " </td> <td> " + v + " </td> </tr>";
                });

                tbTmp = tbTmp.replace("{tbody}", tbody);
                
                $("#show-electric").append(tbTmp);
            });
        }
        else {
            alert("加载电厂失败，请检查网络是否正常！");
        }  
    });
}

