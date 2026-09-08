(function () {
    "use strict";

    /* basic heatmap chart */
    function generateData(count, yrange) {
        var i = 0;
        var series = [];
        while (i < count) {
            var x = 'w' + (i + 1).toString();
            var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push({
                x: x,
                y: y
            });
            i++;
        }
        return series;
    }
    var options = {
        series: [{
            name: '1Am',
            data: generateData(7, {
                min: 0,
                max: 90
            })
        },
        {
            name: '4Am',
            data: generateData(7, {
                min: 0,
                max: 90
            })
        },
        {
            name: '8Am',
            data: generateData(7, {
                min: 0,
                max: 90
            })
        },
        {
            name: '12Pm',
            data: generateData(7, {
                min: 0,
                max: 90
            })
        },
        {
            name: '3Pm',
            data: generateData(7, {
                min: 0,
                max: 90
            })
        },
        {
            name: '7Pm',
            data: generateData(7, {
                min: 0,
                max: 90
            })
        },
        {
            name: '12Am',
            data: generateData(7, {
                min: 0,
                max: 90
            })
        },
     
    
        ],
        chart: {
            height: 335,
            type: 'heatmap',
        },
        dataLabels: {
            enabled: false
        },
        colors: ["#2E90FA"],
        grid: {
            borderColor: '#f2f5f7',
        },
        title: {
            text: 'HeatMap Chart (Single color)',
            align: 'left',
            style: {
                fontSize: '14px',
                fontWeight: 'normal',
                color: '#888'
            },
        },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#888",
                    fontSize: '14px',
                    fontWeight: 400,
                    cssClass: 'apexcharts-xaxis-label',
                },
            }
        },
        yaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#888",
                    fontSize: '12px',
                    fontWeight: 400,
                    cssClass: 'apexcharts-yaxis-label',
                },
            }
        }
    };
    var chart = new ApexCharts(document.querySelector("#heatmap-basic"), options);
    chart.render();

    /* multi series heatmap chart */
    function generateData(count, yrange) {
        var i = 0;
        var series = [];
        while (i < count) {
            var x = (i + 1).toString();
            var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push({
                x: x,
                y: y
            });
            i++;
        }
        return series;
    }
    var data = [
        {
            name: 'W1',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W2',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W3',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W4',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W5',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W6',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W7',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W8',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W9',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W10',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W11',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W12',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W13',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W14',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W15',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        }
    ]
    data.reverse()
    var colors = ["#845adf", "#F27036", "#663F59", "#6A6E94", "#4E88B4", "#00A7C6", "#18D8D8", '#A9D794', '#46AF78', '#A93F55', '#8C5E58', '#2176FF', '#33A1FD', '#7A918D', '#BAFF29']
    colors.reverse()
    var options = {
        series: data,
        chart: {
            height: 350,
            type: 'heatmap',
        },
        dataLabels: {
            enabled: false
        },
        colors: colors,
        xaxis: {
            type: 'category',
            categories: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '01:00', '01:30']
        },
        title: {
            text: 'HeatMap Chart (Different color shades for each series)',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        grid: {
            padding: {
                right: 20
            },
            borderColor: '#f2f5f7',
        },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-xaxis-label',
                },
            }
        },
        yaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-yaxis-label',
                },
            }
        }
    };
var chartEl = document.querySelector("#heatmap-multiseries");
if (chartEl) {
  var chart = new ApexCharts(chartEl, options);
  chart.render();
} else {
}


    /* color range heatmap */
    function generateData(count, yrange) {
        var i = 0;
        var series = [];
        while (i < count) {
            var x = (i + 1).toString();
            var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push({
                x: x,
                y: y
            });
            i++;
        }
        return series;
    }
    var options = {
        series: [{
            name: 'Jan',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'Feb',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'Mar',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'Apr',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'May',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'Jun',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'Jul',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'Aug',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        },
        {
            name: 'Sep',
            data: generateData(20, {
                min: -30,
                max: 55
            })
        }
        ],
        chart: {
            height: 350,
            type: 'heatmap',
        },
        plotOptions: {
            heatmap: {
                shadeIntensity: 0.5,
                radius: 0,
                useFillColorAsStroke: true,
                colorScale: {
                    ranges: [{
                        from: -30,
                        to: 5,
                        name: 'low',
                        color: '#845adf'
                    },
                    {
                        from: 6,
                        to: 20,
                        name: 'medium',
                        color: '#23b7e5'
                    },
                    {
                        from: 21,
                        to: 45,
                        name: 'high',
                        color: '#f5b849'
                    },
                    {
                        from: 46,
                        to: 55,
                        name: 'extreme',
                        color: '#49b6f5'
                    }
                    ]
                }
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: '',
        },
        stroke: {
            width: 1
        },
        title: {
            text: 'HeatMap Chart with Color Range',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-xaxis-label',
                },
            }
        },
        yaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-yaxis-label',
                },
            }
        }
    };
  var colorRangeEl = document.querySelector("#heatmap-colorrange");
if (colorRangeEl) {
  var chartColorRange = new ApexCharts(colorRangeEl, options);
  chartColorRange.render();
} else {
  ;
}

    /* heatmap range without shades */
    var options = {
        series: [{
            name: 'Metric1',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric2',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric3',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric4',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric5',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric6',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric7',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric8',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'Metric8',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        }
        ],
        chart: {
            height: 350,
            type: 'heatmap',
        },
        stroke: {
            width: 0
        },
        plotOptions: {
            heatmap: {
                radius: 30,
                enableShades: false,
                colorScale: {
                    ranges: [{
                        from: 0,
                        to: 50,
                        color: '#845adf'
                    },
                    {
                        from: 51,
                        to: 100,
                        color: '#23b7e5'
                    },
                    ],
                },

            }
        },
        grid: {
            borderColor: '#f2f5f7',
        },
        dataLabels: {
            enabled: true,
            style: {
                colors: ['#fff']
            }
        },
        xaxis: {
            type: 'category',
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-xaxis-label',
                },
            }
        },
        yaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-yaxis-label',
                },
            }
        },
        title: {
            text: 'Rounded (Range without Shades)',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
    };
  var rangeEl = document.querySelector("#heatmap-range");
if (rangeEl) {
  var chartRange = new ApexCharts(rangeEl, options);
  chartRange.render();
} else {
}

})();