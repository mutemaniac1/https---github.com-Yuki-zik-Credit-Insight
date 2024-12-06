<template>
  <div>
    <div id="statistics">
      <div id="chart-container">
        <h style="font-size:larger;font-weight: 800;">时空与非时空数据统计</h>
        <div id="chart1" style="width: 400px; height: 320px;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  data() {
    return {
      spatialCount: 0,
      nonSpatialCount: 0,
      spatialSizeMB: 0,
      nonSpatialSizeMB: 0,
      resources: [],
      formatCount: {
        spatial: {},
        nonSpatial: {},
      },
      categoryCount: {
        基础时空数据: 0,
        公共专题数据: 0,
        城市感知数据: 0,
        课题成果数据: 0,
        子类: {},
      },
      spatialFormats: [
        'tiff', 'jp2', 'img', 'grib', 'shp', 'dxf', 'gdb', 'geojson', 'hdf5',
        'nc', 'obj', 'fbx', 'max', 'ply', 'las', 'xyz', 'png', 'jpg', 'mvt',
        'uasset', 'osgb', 'json'
      ],
      nonSpatialFormats: [
        'xls', 'csv', 'mdb', 'dbf', 'txt', 'doc', 'pdf', 'xml', 'h5', 'npy',
        'onnx', 'pth', 'db', 'dump', 'ttl', 'owl'
      ],
      categoryMappings: {
        基础时空数据: ['基础地理数据', '三维模型数据', '地理切片数据'],
        公共专题数据: ['国土空间数据', '社会经济数据', '城市交通数据', '生态环境数据', '安全保障数据', '历史文化数据'],
        城市感知数据: ['物联感知数据', '社会感知数据', '互联网在线数据'],
        课题成果数据: ['识别成果数据', '评估成果数据', '优化成果数据']
      },
      isShowingSpatial: true,
    };
  },
  mounted() {
    this.fetchResources(); // 从服务器获取数据
  },
  methods: {
    async fetchResources() {
      try {
        const response = await fetch('/api/systemtable/api/selectAllData');
        if (!response.ok) {
          throw new Error('Failed to fetch resources');
        }

        const textData = await response.text();
        let formattedData = textData.trim();

        if (formattedData.endsWith(';')) {
          formattedData = formattedData.slice(0, -1);
        }

        formattedData = `[${formattedData}]`;
        const data = JSON.parse(formattedData);

        if (Array.isArray(data)) {
          this.resources = data;
          this.calculateStatistics(); // 数据获取后统计
        } else {
          console.error('Expected an array, but got:', typeof data);
        }
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
    calculateStatistics() {
      this.spatialCount = 0;
      this.nonSpatialCount = 0;
      this.spatialSizeMB = 0;
      this.nonSpatialSizeMB = 0;
      this.formatCount.spatial = {};
      this.formatCount.nonSpatial = {};
      this.categoryCount = {
        基础时空数据: 0,
        公共专题数据: 0,
        城市感知数据: 0,
        课题成果数据: 0,
        子类: {},
      };

      this.resources.forEach((resource) => {
        const format = resource.format.toLowerCase();
        const sizeMB = (resource.filesize / (1024 * 1024)).toFixed(2);
        const isSpatialFormat = this.spatialFormats.includes(format);
        const isSpatialResource = resource.space === "是";

        if (isSpatialFormat ) {
          this.spatialCount++;
          this.spatialSizeMB += parseFloat(sizeMB);
          this.formatCount.spatial[format] = (this.formatCount.spatial[format] || 0) + 1;
        } else {
          this.nonSpatialCount++;
          this.nonSpatialSizeMB += parseFloat(sizeMB);
          this.formatCount.nonSpatial[format] = (this.formatCount.nonSpatial[format] || 0) + 1;
        }

        const fileType = resource.fileType;
        const subCategory = resource.subCategory;

        if (this.categoryMappings[fileType]) {
          this.categoryCount[fileType]++;
          this.categoryCount.子类[subCategory] = (this.categoryCount.子类[subCategory] || 0) + 1;
        }
      });

      this.renderSpatialNonSpatialChart(); // 计算完毕后重新渲染图表
    },
    renderSpatialNonSpatialChart() {
      const chart1 = echarts.init(document.getElementById('chart1'));

      const option1 = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} MB ({d}%)'
        },
        title: {
          text: `时空数据大小: ${this.spatialSizeMB.toFixed(2)} MB\n\n非时空数据大小: ${this.nonSpatialSizeMB.toFixed(2)} MB`,
          left: 'right',
          top: 'top',
          textStyle: {
            fontSize: 13,
            fontWeight: 'bold',
            color:' #888',
          },
          padding: [5, 10]
        },
        legend: {
          data: ['时空数据', '非时空数据'],
          orient: 'vertical',
          top: 'center',
          left: 'left'
        },
        series: [
          {
            name: '数据类型',
            type: 'pie',
            radius: '60%',
            center: ['70%', '60%'],
            label: {
              position: 'inner',
              fontSize: 12
            },
            labelLine: {
              show: false
            },
            data: [
              { value: this.spatialSizeMB.toFixed(2), name: '时空数据', selected: this.isShowingSpatial },
              { value: this.nonSpatialSizeMB.toFixed(2), name: '非时空数据', selected: !this.isShowingSpatial }
            ]
          }
        ]
      };

      chart1.setOption(option1);

      chart1.on('legendselectchanged', (params) => {
        if (params.name === '时空数据') {
          this.isShowingSpatial = true;
          this.renderSpatialNonSpatialChart();
        } else if (params.name === '非时空数据') {
          this.isShowingSpatial = false;
          this.renderSpatialNonSpatialChart();
        }
      });
    },
  },
};
</script>

<style scoped>
#statistics {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

#chart-container {
  width: 48%;
}

#chart1 {
  margin-top: 20px;
}
</style>
