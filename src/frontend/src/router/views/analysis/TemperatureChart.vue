<template>
  <div ref="chart" style="width: 100%; height: 300px;"></div>
</template>

<script>
import * as echarts from "echarts";

export default {
  props: {
    temperatureData: Array, // 温度数据
    secondaryTemperatureData: Array, // 全量数据对应的温度
    timeStamps: Array, // 时间戳
    ids: String // 设备ID
  },
  data() {
    return {
      chart: null
    };
  },
  methods: {
    initChart() {
      if (!this.chart) {
        this.chart = echarts.init(this.$refs.chart);
      }

      // 获取实时数据和全量数据
      const realTimeData = this.temperatureData;


      // 获取时间戳，确保长度与温度数据一致
      const realTimeTimestamps = this.timeStamps.slice(-realTimeData.length); // 最后N个时间戳
    

      // 合并实时数据和全量数据
     

      // 包装数据，添加标识以及对应时间戳
      const wrappedData = realTimeData.map((item, index) => {
        return {
          value: item,
          type: index < 300 ? '实时数据' : '预测数据', // 标识数据类型
          timestamp: realTimeTimestamps[index] // 对应时间戳
        };
      });

      // 配置图表选项
      const options = {
        title: {
          text: `[${this.ids}] 温度趋势图`,
          left: "center"
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            let tip = '';
            params.forEach((param) => {
              tip += `${param.seriesName} - ${param.data.value}℃ (${param.data.type}) 时间: ${param.data.timestamp}<br>`;
            });
            return tip;
          }
        },
        xAxis: {
          type: "category",
          data: realTimeTimestamps, // 合并后的时间戳
          axisLabel: {
            rotate: 45,
            fontSize: 10
          }
        },
        yAxis: {
          type: "value",
          axisLabel: {
            formatter: "{value}℃"
          }
        },
        series: [
          {
            name: "温度",
            type: "line",
            data: wrappedData,
            smooth: true,
            lineStyle: {
              color: "#FF6347" // 实时数据折线颜色
            },
            areaStyle: {
              opacity: 0.2,
              color: "#FF6347"
            },
            markLine: {
              symbol: 'circle', // 标记点样式
              symbolSize: 10, // 标记点大小
              data: [
                { 
                  xAxis: 300, // 在第300个点的位置添加标记
                  label: {
                    show: true,
                    position: 'middle',
                    formatter: '预测' ,// 显示的名称
                    rotate: 90, // 文字旋转90度
        align: 'left', // 水平对齐方式
        verticalAlign: 'middle' // 垂直对齐方式
       
                  }
                }
              ]
            }
          }
        ]
      };

      this.chart.setOption(options);
    }
  },
  watch: {
    temperatureData() {
      this.initChart();
    },
    secondaryTemperatureData() {
      this.initChart();
    },
    timeStamps() {
      this.initChart();
    }
  },
  mounted() {
    this.initChart();
  }
};
</script>
