<script>
import Layout from "../../layouts/main";
import PageHeader from "@/components/page-header";
import appConfig from "@/app.config";
import { getAllIot } from '../../../api';
import * as XLSX from 'xlsx';



/**
 * 历史信息组件
 */
export default {
  page: {
    title: "历史数据",
    meta: [{ name: "description", content: appConfig.description }]
  },
  components: { Layout, PageHeader },
  data() {
    return {
      title: "历史数据",
      items: [
        {
          text: "温湿度监测系统",
          href: "/"
        },
        {
          text: "历史数据",
          active: true
        }
      ],
      totalRows: 1,
      currentPage: 1,
      perPage: 10,
      pageOptions: [10, 25, 50, 100],
      filter: null,
      filterOn: [],
      sortBy: "age",
      sortDesc: false,
      fields: [
        { key: "设备ID", sortable: true },
        { key: "时间", sortable: true },
        { key: "温度", label: "温度（℃）", sortable: true },  // 修改为温度（℃）
        { key: "湿度", label: "湿度（%）", sortable: true }   // 修改为湿度（%）
      ],
      tableData: [
      ]
    };
  },
  computed: {
    /**
     * Total no. of records
     */
    rows() {
      return this.tableData.length;
    }
  },
  mounted() {
    // Set the initial number of items
    this.totalRows = this.items.length;

    console.log(localStorage.getItem('mqttData'));
    const savedData = localStorage.getItem('mqttData');
    if (savedData) {
      // 如果有数据，加载到表格中
      this.tableData = JSON.parse(savedData);
      this.totalRows = this.tableData.length;
    } else {
      // 如果没有数据，从 Excel 文件中读取
      this.readExcelFile();
    }

  },
  methods: {

    /**
     * Search the table data with search input
     */
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
    readExcelFile() {


      const filePath = '/mqtt_data.xlsx'; // 假设文件放在 public 文件夹下
      fetch(filePath)
        .then(response => {
          if (!response.ok) {
            throw new Error('文件未找到！');
          }
          return response.arrayBuffer();
        })
        .then(buffer => {
          const workbook = XLSX.read(buffer, { type: 'array' });
          const sheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[sheetName];
          const excelData = XLSX.utils.sheet_to_json(worksheet);

          // 处理前 100 条数据
          const processedData = excelData.slice(0, 100).map((row, index) => ({
            设备ID: index < 50 ? '设备1' : '设备2',
            时间: row['Timestamp'] || '未知时间', // 直接作为字符串读取
            温度: parseFloat(row['Temperature'] || 0).toFixed(2),
            湿度: parseFloat(row['Humidity'] || 0).toFixed(2)
          }));

          // 加载数据到表格
          this.tableData = processedData.slice(0, 50); // 显示前 50 条数据
          this.totalRows = this.tableData.length;

          // 存储到 localStorage
          localStorage.setItem('mqttData', JSON.stringify(processedData));

        })
        .catch(error => {
          console.error('读取文件失败:', error);
          this.$message({
            type: 'error',
            message: '读取文件失败，请确保 mqtt_data.xlsx 文件存在！'
          });
        });
    }
    ,
    outputXLSX() {
      // 从 localStorage 获取数据
      const savedData = localStorage.getItem('mqttData');
      if (!savedData) {
        this.$message({
          type: 'error',
          message: '没有可导出的数据！'
        });
        return;
      }

      const tableData = JSON.parse(savedData);

      // 创建 Excel 工作簿并添加数据
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(tableData);
      XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

      // 导出为 mqtt_data.xlsx
      XLSX.writeFile(wb, 'mqtt_data.xlsx');

      this.$message({
        type: 'success',
        message: '导出成功！'
      });
    }

    ,
    outputAbnormalData() {
      getAllIot().then(({ data }) => {
        var dict_maxtemp = {}
        var dict_mintemp = {}
        var dict_maxhumi = {}
        var dict_minhumi = {}
        var iots = data.data
        iots.forEach(element => {
          var id = (element.hardid)
          dict_maxtemp[id] = element.tempmax
          dict_mintemp[id] = element.tempmin
          dict_maxhumi[id] = element.humimax
          dict_minhumi[id] = element.humimin
        });

        const wb = XLSX.utils.book_new();
        const processedData = []
        this.tableData.forEach(element => {
          var curId = parseInt(element.设备ID)
          var curTemp = parseFloat(element.温度)
          var curHumi = parseFloat(element.湿度)
          var items = {
            设备ID: element.设备ID,
            时间: element.时间,
            温度: element.温度,
            湿度: element.湿度,
            状态: '',
            正常温度范围: '',
            正常湿度范围: ''
          }
          items.正常温度范围 = dict_mintemp[curId] + '~' + dict_maxtemp[curId]
          items.正常湿度范围 = dict_minhumi[curId] + '~' + dict_maxhumi[curId]
          if (!(dict_mintemp[curId] <= curTemp && curTemp <= dict_maxtemp[curId])) {
            if (!(dict_minhumi[curId] <= curHumi && curHumi <= dict_maxhumi[curId])) {
              items.状态 = '温湿度异常'
            } else {
              items.状态 = '温度异常'
            }
          } else {
            if (!(dict_minhumi[curId] <= curHumi && curHumi <= dict_maxhumi[curId])) {
              items.状态 = '湿度异常'
            } else {
              items.状态 = ''
            }
          }
          if (items.状态 != '') {
            processedData.push(items)
          }
        });

        const ws = XLSX.utils.json_to_sheet(processedData);
        XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
        XLSX.writeFile(wb, "AbnormalRecords.xlsx");
      })
    }
  }
};
</script>

<template>
  <Layout>
    <PageHeader :title="title" :items="items" />

    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">数据条目</h4>
            <p class="card-title-desc"></p>
            <div class="row mb-md-2">
              <div class="col-sm-12 col-md-6">
                <div id="tickets-table_length" class="dataTables_length">
                  <label class="d-inline-flex align-items-center">
                    Show
                    <b-form-select class="form-control form-control-sm form-select form-select-sm" v-model="perPage"
                      size="sm" :options="pageOptions"></b-form-select>entries
                  </label>
                </div>
              </div>
              <!-- Search -->
              <div class="col-sm-12 col-md-6">
                <div id="tickets-table_filter" class="dataTables_filter text-md-end">
                  <label class="d-inline-flex align-items-center">
                    Search:
                    <b-form-input v-model="filter" type="search" placeholder="Search..."
                      class="form-control form-control-sm ml-2"></b-form-input>
                  </label>
                </div>
              </div>
              <div style="margin-top: 15px;">
                数据共 {{ this.tableData.length }} 条 &nbsp; <b-button variant="outline-primary"
                  @click="outputXLSX">导出报表</b-button>
                <b-button variant="outline-primary" @click="outputAbnormalData"
                  style="margin-left: 10px;">导出异常数据</b-button>
              </div>
              <!-- End search -->
            </div>

            <!-- Table -->
            <div class="table-responsive mb-0 datatables">
              <b-table :items="tableData" :fields="fields" responsive="sm" :per-page="perPage"
                :current-page="currentPage" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" :filter="filter"
                :filter-included-fields="filterOn" @filtered="onFiltered"></b-table>
            </div>

            <div class="row">
              <div class="col">
                <div class="dataTables_paginate paging_simple_numbers float-end">
                  <ul class="pagination pagination-rounded mb-0">
                    <!-- pagination -->
                    <b-pagination v-model="currentPage" :total-rows="rows" :per-page="perPage"></b-pagination>
                  </ul>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>