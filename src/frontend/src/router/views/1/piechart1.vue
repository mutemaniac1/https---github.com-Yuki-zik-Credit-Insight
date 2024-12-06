<template>
  <div>
    <div id="statistics">
      <div id="chart-container">
        <div class="header">
          <h style="font-size: larger; font-weight: 800;">数据类型统计</h>
          <button 
            v-if="currentCategory === '子类'" 
            @click="returnToMainCategory"
            class="return-button"
          >
            返回主类
          </button>
        </div>
        <div id="chart2" style="width: 400px; height: 320px;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  data() {
    return {
      categorySize: {
        基础时空数据: 0,
        公共专题数据: 0,
        城市感知数据: 0,
        课题成果数据: 0,
        子类: {},
      },
      categoryMappings: {
        基础时空数据: ['基础地理数据', '三维模型数据', '地理切片数据'],
        公共专题数据: ['国土空间数据', '社会经济数据', '城市交通数据', '生态环境数据', '安全保障数据', '历史文化数据'],
        城市感知数据: ['物联感知数据', '社会感知数据', '互联网在线数据'],
        课题成果数据: ['识别成果数据', '评估成果数据', '优化成果数据']
      },
      currentCategory: '主类', // 用于标记当前展示的是主类还是子类
      selectedMainCategory: null, // 当前选择的主类
      resources: []
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
          this.calculateStatistics(); // 数据获取后进行统计计算
          this.renderCategoryChart(); // 计算完毕后绘制图表
        } else {
          console.error('Expected an array, but got:', typeof data);
        }
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },

    calculateStatistics() {
      // 初始化统计数据
      this.categorySize = {
        基础时空数据: 0,
        公共专题数据: 0,
        城市感知数据: 0,
        课题成果数据: 0,
        子类: {},
      };

      // 遍历资源数据进行分类统计
      this.resources.forEach((resource) => {
        const fileType = resource.type;
        const subCategory = resource.subCategory;
        const size = (resource.filesize || 0) / (1024 * 1024); // 将字节转换为 MB

        // 确保主类和子类都存在
        if (this.categoryMappings[fileType]) {
          this.categorySize[fileType] += size;
          this.categorySize.子类[subCategory] = (this.categorySize.子类[subCategory] || 0) + size;
        }
      });

      // 保留两位小数
      Object.keys(this.categorySize).forEach(category => {
        if (typeof this.categorySize[category] === 'number') {
          this.categorySize[category] = this.categorySize[category].toFixed(2);
        } else {
          Object.keys(this.categorySize[category]).forEach(subCategory => {
            this.categorySize[category][subCategory] = this.categorySize[category][subCategory].toFixed(2);
          });
        }
      });
    },

    renderCategoryChart() {
      const chart2 = echarts.init(document.getElementById('chart2'));

      const mainCategories = Object.keys(this.categorySize).filter(c => c !== '子类');
      const subCategories = this.selectedMainCategory ? this.categoryMappings[this.selectedMainCategory] : [];

      // 主类和子类数据分别处理
      const data = this.currentCategory === '主类'
        ? mainCategories.map(category => ({
            name: category,
            value: parseFloat(this.categorySize[category]),
          })).filter(item => item.value > 0) // 过滤掉值为0的类别
        : subCategories.map(subCategory => ({
            name: subCategory,
            value: parseFloat(this.categorySize.子类[subCategory]),
          })).filter(item => item.value > 0); // 过滤掉值为0的子类别

      const option2 = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c}MB ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'center',
          data: this.currentCategory === '主类' ? mainCategories : subCategories,
          selectedMode: false, // 禁用图例的点击功能
        },
        series: [
          {
            name: this.currentCategory,
            type: 'pie',
            radius: '70%',
            center: ['70%', '50%'],
            data: [...data],
            label: {
              show: false, // 隐藏饼图上的标签文字
            },
            labelLine: {
              show: false, // 隐藏引导线
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              }
            }
          }
        ]
      };

      chart2.setOption(option2);

      // 添加点击事件，仅在主类视图时点击进入子类视图
      chart2.off('click'); // 确保没有重复绑定
      chart2.on('click', (params) => {
        if (this.currentCategory === '主类' && this.categoryMappings[params.name]) {
          this.selectedMainCategory = params.name;
          this.currentCategory = '子类';
          this.renderCategoryChart(); // 重新绘制图表，进入子类视图
        }
      });
    },

    returnToMainCategory() {
      this.currentCategory = '主类';
      this.selectedMainCategory = null;
      this.renderCategoryChart(); // 重新绘制图表，返回主类视图
    }
  }
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
  position: relative;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#chart2 {
  margin-top: 20px;
}

.return-button {
  padding: 3px 6px;
  padding-top: 3px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.return-button:hover {
  background-color: #0056b3;
}
</style>
