<template>
  <div>
    <el-row class="navbar" type="flex" justify="space-between" align="middle">
  <el-col :span="7" class="navbar-left">
    <span class="logo">城市存量空间数据场景化<br>集成与一体化管理系统</span>
  </el-col>
  <el-col :span="9" class="navbar-center">
    <el-menu mode="horizontal" default-active="5" class="el-menu-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="1"><router-link to="/system/admin">首页</router-link></el-menu-item>
      <el-menu-item index="2"><router-link to="/system/resourse">数据要素</router-link></el-menu-item>
      <el-menu-item index="3"><router-link to="/system/tileset">地图切片</router-link></el-menu-item>
      <el-menu-item index="4"><router-link to="/system/scene">场景集成</router-link></el-menu-item>
      <el-menu-item index="5"><router-link to="/system/services">数据服务</router-link></el-menu-item>
    </el-menu>
  </el-col>
  <el-col :span="8" class="navbar-right" style="text-align: right;">
    <span class="user-info">{{ username }}</span>
    <el-button type="danger" @click="logout">退出</el-button>
  </el-col>
</el-row>

    <el-card>
      <div class="content">
        <h1>服务列表</h1>

        <el-row class="search-box">
          <el-col :span="8">
            <el-button type="primary" @click="showUploadModal">发布要素服务</el-button>
            <el-button type="primary" @click="showUploadModal1">发布场景服务</el-button>
          </el-col>
          <el-col :span="8">
            <el-input v-model="searchQuery" placeholder="搜索资源..."></el-input>
          </el-col>
          <el-col :span="8">
            <el-button type="primary" @click="searchResource">搜索</el-button>
            <el-button @click="refreshData">刷新</el-button>
          </el-col>
        </el-row>

        
        <el-table :data="paginatedservices" style="width: calc(100% - 40px); margin: 0 20px;">
          <el-table-column prop="serviceName" label="服务名称"></el-table-column>
          <el-table-column prop="serviceType" label="服务类型"></el-table-column>
          <el-table-column prop="serviceDescription" label="描述"></el-table-column>
          <el-table-column prop="datasource" label="数据源"></el-table-column>
          <el-table-column prop="user" label="发布者"></el-table-column> 
          <el-table-column prop="date" label="发布日期"></el-table-column>
          <el-table-column prop="shareStatus" label="共享状态"></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <div class="actions">
                <div class="action-row">
                  <el-button size="mini" class="compact-button" @click="urlResource(scope.row)">URL</el-button>
                  <el-button size="mini" class="compact-button" @click="editResource(scope.row)">预览</el-button>
                </div>
                <div class="action-row">
                  <el-button size="mini" type="danger" class="compact-button" @click="confirmDelete(scope.row)">删除</el-button>
                  <el-button size="mini" type="primary" class="compact-button" @click="downloadResource(scope.row)">下载</el-button>
                </div>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 12, 15]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="services.length">
        </el-pagination>
      </div>
    </el-card>

  

    <el-dialog
  title="发布要素服务"
  :visible.sync="uploadDialogVisible"
  width="35%"
  @close="resetUploadForm">
  <el-form :model="uploadForm" label-width="130px" class="elform">
    <div class="button-container">
        <el-button type="primary" class="custom-button" @click="showSelectSourceModal">选择数据源</el-button>
      </div>
    <el-form-item label="数据源">
  <el-input v-model="uploadForm.datasource" placeholder="请选择数据源" readonly class="custom-input"></el-input>
</el-form-item>
    <el-form-item label="服务名称">
      <el-input v-model="uploadForm.serviceName" class="custom-input"></el-input>
    </el-form-item>
    <el-form-item label="服务类型">
      <el-select v-model="uploadForm.serviceType" placeholder="请选择" class="custom-input">
        <el-option label="wms" value="wms"></el-option>
        <el-option label="wfs" value="wfs"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="服务描述">
      <el-input type="textarea" v-model="uploadForm.serviceDescription" class="custom-input"></el-input>
    </el-form-item>
    <el-form-item label="共享状态">
      <el-select v-model="uploadForm.shareState" placeholder="请选择" class="custom-input">
        <el-option label="共享" value="共享"></el-option>
        <el-option label="不共享" value="不共享"></el-option>
      </el-select>
    </el-form-item>
    
   

        </el-form>

        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="submitForm">确认发布</el-button>
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          
        </div>
</el-dialog>

<el-dialog
  title="发布场景服务"
  :visible.sync="uploadDialogVisible1"
  width="35%"
  @close="resetUploadForm">
  <el-form :model="uploadForm" label-width="130px" class="elform">
    <div class="button-container">
        <el-button type="primary" class="custom-button" @click="showSelectSourceModal1">选择数据源</el-button>
      </div>
    <el-form-item label="数据源">
  <el-input v-model="uploadForm.datasource" placeholder="请选择数据源" readonly class="custom-input"></el-input>
</el-form-item>
    <el-form-item label="服务名称">
      <el-input v-model="uploadForm.serviceName" class="custom-input"></el-input>
    </el-form-item>
    <el-form-item label="服务类型">
      <el-select v-model="uploadForm.serviceType" placeholder="请选择" class="custom-input">
        <el-option label="wms" value="wms"></el-option>
        <el-option label="wfs" value="wfs"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="服务描述">
      <el-input type="textarea" v-model="uploadForm.serviceDescription" class="custom-input"></el-input>
    </el-form-item>
    <el-form-item label="共享状态">
      <el-select v-model="uploadForm.shareState" placeholder="请选择" class="custom-input">
        <el-option label="共享" value="共享"></el-option>
        <el-option label="不共享" value="不共享"></el-option>
      </el-select>
    </el-form-item>
    
   

        </el-form>

        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="submitForm">确认发布</el-button>
          <el-button @click="uploadDialogVisible1 = false">取消</el-button>
          
        </div>
</el-dialog>


    <!-- 服务设置弹窗 -->
    <el-dialog
      title="服务设置"
      :visible.sync="serviceSettingsDialogVisible"
      width="30%"
      @close="resetServiceSettingsForm">
      <el-form :model="serviceSettingsForm" label-width="120px">
        <el-form-item label="服务类型">
          <el-select v-model="serviceSettingsForm.serviceType" placeholder="请选择服务类型">
            <el-option label="mvt" value="mvt"></el-option>
            <el-option label="wfs" value="wfs"></el-option>
            <el-option label="wms" value="wms"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="服务名称">
          <el-input v-model="serviceSettingsForm.serviceName"></el-input>
        </el-form-item>
        <el-form-item label="服务描述">
          <el-input type="textarea" v-model="serviceSettingsForm.serviceDescription"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="confirmServiceSettings">确定</el-button>
        <el-button @click="resetServiceSettingsForm">取消</el-button>
        
      </span>
    </el-dialog>

    <el-dialog
  title="服务 URL"
  :visible.sync="urlDialogVisible"
  width="50%"
  @close="resetUrlDialog">
  <el-input type="textarea" v-model="serviceUrl" readonly></el-input>
  <span slot="footer" class="dialog-footer">
    <!--<el-button @click="copyWMSUrl">复制 WMS</el-button>-->
    <el-button @click="copyUrl">复制</el-button>
    <el-button @click="resetUrlDialog">取消</el-button>
  </span>
</el-dialog>



<!-- 数据源选择弹窗 -->
<!-- 数据源选择弹窗 -->
<el-dialog
  title="选择数据源"
  :visible.sync="selectSourceDialogVisible"
  width="50%"
  @close="handleClose">

  <div style="display: flex; margin-bottom: 20px;">
    <el-input
      v-model="sourceSearchQuery"
      placeholder="搜索数据源..."
      style="flex: 1; margin-right: 10px;">
    </el-input>
    <el-button type="primary" @click="searchResource1">搜索</el-button>
    <el-button type="success" @click="fetchResources">刷新</el-button>
  </div>

  <el-table :data="paginatedResources" style="width: 100%">
    <el-table-column label="选择" width="60px">
      <template slot-scope="scope">
        <el-checkbox
          v-model="selectedSourceIds"
          :label="scope.row.pid"
          class="hidden-checkbox">
          <!-- 隐藏实际的label内容 -->
          <span class="hidden-label">{{ scope.row.pid }}</span>
        </el-checkbox>
      </template>
    </el-table-column>
    <el-table-column prop="name" label="数据名称"></el-table-column>
    <el-table-column prop="type" label="数据类别"></el-table-column>
    <el-table-column prop="success" label="入库信息">
      <template slot-scope="scope">
        <span>{{ scope.row.state ? '已入库' : '未入库' }}</span>
      </template>
    </el-table-column>
  </el-table>

  <div class="pagination-container">
    <el-pagination
      @size-change="handleSizeChange2"
      @current-change="handlePageChange2"
      :current-page="currentPage2"
      :page-size="pageSize2"
      :total="filteredSources.length"
      layout="total, sizes, prev, pager, next, jumper"
      :page-sizes="[5, 10]"
    >
    </el-pagination>
  </div>

  <div slot="footer" class="dialog-footer">
    <el-button type="primary" @click="confirmSelection">确认选择</el-button>
    <el-button @click="handleCancel">取消</el-button>
  </div>
</el-dialog>




<el-dialog
  title="选择数据源"
  :visible.sync="selectSourceDialogVisible1"
  width="50%"
  @close="cancelSelection1">

  <!-- 搜索框和按钮 -->
  <el-input
    v-model="sourceSearchQuery1"
    placeholder="搜索数据源..."
    style="margin-bottom: 20px;">
  </el-input>
  <el-button type="primary" @click="searchResource2">搜索</el-button>
  <el-button @click="fetchscenes">刷新</el-button>

  <!-- 数据表格 -->
  <el-table
    :data="paginatedResources1"
    style="width: 100%"
    ref="dataTable"
    @selection-change="handleSelectionChange1"
    :row-key="row => row.pid">
    <el-table-column type="selection" width="60px"></el-table-column>
    <el-table-column prop="sceneName" label="数据名称"></el-table-column>
    <el-table-column prop="sceneType" label="数据类型"></el-table-column>
    <el-table-column prop="success" label="入库信息">
      <template slot-scope="scope">
        <span>已入库</span>
      </template>
    </el-table-column>
  </el-table>

  <!-- 分页 -->
  <div class="pagination-container">
    <el-pagination
      @size-change="handleSizeChange1"
      @current-change="handlePageChange1"
      :current-page="currentPage1"
      :page-size="pageSize1"
      :total="filteredSources1.length"
      layout="total, sizes, prev, pager, next, jumper"
      :page-sizes="[5, 10]">
    </el-pagination>
  </div>

  <!-- 弹窗底部按钮 -->
  <div slot="footer" class="dialog-footer">
    <el-button type="primary" @click="confirmSelection1">确认选择</el-button>
    <el-button @click="cancelSelection1">取消</el-button>
  </div>
</el-dialog>




  </div>
</template>

<script>

import { generatePID } from './pidGenerator';
export default {
  data() {
    return {
      scenes:[],
      resources: [],
      currentPage1: 1, // 当前页码
      pageSize1: 5,
      pageSize2: 5, // 每页显示的项数
      deleteDialogVisible: false,
    resourceToDelete: null, 
      username: localStorage.getItem('username'),// 读取存储的用户名
      region : localStorage.getItem('region'),
      uploadDialogVisible1: false,
      urlDialogVisible: false,
    serviceUrl: '',
      searchQuery: '',
      filteredResources:[],
      singleLayerSearchQuery: '',
      multipleLayersSearchQuery: '',
      singleLayerDialogVisible: false,
      multipleLayersDialogVisible: false,
      serviceSettingsDialogVisible: false,
      currentPage: 1,
      currentPage2: 1,
      pageSize: 5,
      singleLayerCurrentPage: 1,
      singleLayerPageSize: 5,
      multipleLayersCurrentPage: 1,
      multipleLayersPageSize: 5,
      selectedSingleLayers: [], // Changed to an array for multiple selections
      selectedMultipleLayers: [],
      serviceSettingsForm: {
        serviceType: '',
        serviceName: '',
        serviceDescription: ''
      },
      selectedSource: [] ,
      selectSourceDialogVisible: false,
      selectSourceDialogVisible1: false,
      sourceSearchQuery: '',
      sourceSearchQuery1: '',
      filteredSources: [],
      paginatedResources:[],
      paginatedResources1:[],
      filteredSources1: [],
      selectedSourceIds:[],
      selectedSourceId: '', 
      selectedSourceId1: '',
      uploadDialogVisible: false,
      paginatedservices: [],
      uploadForm: {
        pid:'',
        serviceName: '',
        serviceType: '',
        serviceDescription: '',
        user: '',
        date: '',
        shareState: '',
        datasource: '' 
      },
      searchQuery: '',
      services: [],
    };
  },
  mounted() {
  this.fetchservices();  // 正确的写法
},

  computed: {
    
    
    
  
    
    filteredSingleLayerResources() {
      return this.singleLayerResources.filter(resource =>
        resource.name.toLowerCase().includes(this.singleLayerSearchQuery.toLowerCase())
      );
    },
    paginatedSingleLayerResources() {
      const start = (this.singleLayerCurrentPage - 1) * this.singleLayerPageSize;
      const end = start + this.singleLayerPageSize;
      return this.filteredSingleLayerResources.slice(start, end);
    },
    filteredMultipleLayersResources() {
      return this.multipleLayersResources.filter(resource =>
        resource.name.toLowerCase().includes(this.multipleLayersSearchQuery.toLowerCase())
      );
    },
    paginatedMultipleLayersResources() {
      const start = (this.multipleLayersCurrentPage - 1) * this.multipleLayersPageSize;
      const end = start + this.multipleLayersPageSize;
      return this.filteredMultipleLayersResources.slice(start, end);
    }
  },
  methods: {
    paginateResources() {
      const start = (this.currentPage2 - 1) * this.pageSize2;
      const end = start + this.pageSize2;
      this.paginatedResources = this.filteredSources.slice(start, end);
    },
    paginateResources1() {
      const start = (this.currentPage1 - 1) * this.pageSize1;
      const end = start + this.pageSize1;
      this.paginatedResources1= this.filteredSources1.slice(start, end);
    },
    paginateservices() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.paginatedservices = this.services.slice(start, end);
    },
    async fetchservices() {
  try {
    const response = await fetch('/api/systemtable/api/selectAllServices');
    if (!response.ok) {
      throw new Error('Failed to fetch services');
    }

    let textData = await response.text();
    console.log('Raw response text:', textData);

    // 处理响应文本，将其转换为有效的 JSON 格式
    let formattedData = textData;

    // 1. 为日期字段（yyyy-mm-dd 格式）加上引号
    formattedData = formattedData.replace(/(\d{4}-\d{2}-\d{2})/g, '"$1"');

    // 2. 处理需要包裹引号的字段，包括中文字符串、特殊字符等
    const fieldNames = ["serviceType", "serviceDescription", "datasource"];
    fieldNames.forEach(field => {
      const regex = new RegExp(`("${field}":)([^",}\\]]+)`, 'g');
      formattedData = formattedData.replace(regex, (match, p1, p2) => {
        // 如果是布尔值或数字，不加引号
        if (p2 === 'true' || p2 === 'false' || !isNaN(p2)) return match;
        // 处理特殊字符和空格的字符串字段
        return `${p1}"${p2.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`; // 处理特殊字符
      });
    });

    // 3. 为布尔值保留原格式，确保不被加引号
    formattedData = formattedData.replace(/\btrue\b/g, 'true').replace(/\bfalse\b/g, 'false');

    // 4. 检查是否需要处理字段的额外规则（例如特定字段加引号）
    formattedData = formattedData.replace(/"([^":]+)":\s*([^,}\]]+)/g, (match, p1, p2) => {
      // 只处理未加引号的值
      if (isNaN(p2) && p2 !== 'true' && p2 !== 'false') {
        return `"${p1}":"${p2.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
      }
      return match; // 如果是数字或布尔值，则保留
    });

    console.log('Formatted data:', formattedData);

    // 尝试解析 JSON 数据
    const data = JSON.parse(formattedData);
    console.log('Parsed data:', data);

    if (Array.isArray(data)) {
  this.services = data;
  // 处理字符串字段，移除多余的引号和转义符
  this.services = this.services.map(service => {
    return {
      ...service,
      serviceName: typeof service.serviceName === 'string' ? service.serviceName.replace(/^"|"$/g, '').replace(/\\"/g, '') : service.serviceName,
      serviceType: typeof service.serviceType === 'string' ? service.serviceType.replace(/^"|"$/g, '').replace(/\\"/g, '') : service.serviceType,
      serviceDescription: typeof service.serviceDescription === 'string' ? service.serviceDescription.replace(/^"|"$/g, '').replace(/\\"/g, '') : service.serviceDescription,
      datasource: typeof service.datasource === 'string' ? service.datasource.replace(/^"|"$/g, '').replace(/\\"/g, '') : service.datasource,
      date: typeof service.date === 'string' ? service.date.replace(/^"|"$/g, '').replace(/\\"/g, '') : service.date,
    };
  });

  this.paginateservices();
}
 else {
      console.error('Expected an array, but got:', typeof data);
    }
  } catch (error) {
    console.error('Error fetching services:', error);
  }
}
,

handleSelectionChange1(val) {
    // 更新选中的 ID 列表
    this.selectedSourceIds = val.map(item => item.pid);
  },
handleSizeChange(newSize) {
    this.pageSize = newSize;
    this.paginateservices();
  },
  
  handleCurrentChange(newPage) {
    this.currentPage = newPage;
    this.paginateservices();
  },
  
  refreshData() {
    this.fetchservices(); 
    this.searchQuery=''; // 重新从服务器获取数据
  },
  async searchResource() {
  const fields = ['serviceName', 'serviceType', 'serviceDescription'];
  const uniqueResults = new Set(); // 使用 Set 来去重字符串化的 JSON 对象
  const jsonRegex = /<div>\s*({.*?})\s*<\/div>/g; // 匹配 JSON 的正则表达式

  try {
    // 遍历每个字段进行模糊搜索
    for (const field of fields) {
      const url = `/api/textquery/fuzzySearch?indexName=service_list&fieldName=${field}&searchTerm=${this.searchQuery}&fuzziness=1`;

      const response = await fetch(url, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch search results for field: ${field}`);
      }

      const textResponse = await response.text();
      console.log('Text response for field:', field, textResponse);

      // 使用正则表达式提取 JSON 字符串
      let match;
      while ((match = jsonRegex.exec(textResponse)) !== null) {
        try {
          const jsonObject = JSON.parse(match[1]); // 解析 JSON 字符串
          uniqueResults.add(JSON.stringify(jsonObject)); // 序列化 JSON 对象并存储到 Set 中
        } catch (err) {
          console.error("Error parsing JSON:", err);
        }
      }
    }

    // 将去重后的结果转化为数组并存储到 filteredResources 中
    this.services = Array.from(uniqueResults).map(item => JSON.parse(item)); // 反序列化为 JSON 对象
    console.log('Final unique services:', this.services);

    this.paginateservices(); // 更新分页数据
  } catch (error) { 
    console.error('Error fetching search results:', error);
  }
},

    handleCancel() {
      this.selectSourceDialogVisible = false;
      this.clearSelection();
      this.resetSelection();
    },
    handleClose() {
      this.clearSelection();
      this.resetSelection();
    },
    clearSelection() {
      this.selectedSourceId = null;
      this.sourceSearchQuery=''; // 清除已选数据
    },
    showUploadModal() {
      this.uploadDialogVisible = true;
    },
    showUploadModal1() {
      this.uploadDialogVisible1 = true;
    },
    showSelectSourceModal() {
      this.selectSourceDialogVisible = true;
      this.fetchResources();
    },
    showSelectSourceModal1() {
      this.selectSourceDialogVisible1 = true;
      this.fetchscenes();

    },
   

    confirmSelection1() {
    // 从过滤后的数据中找出选中的项
    const selectedSources = this.filteredSources1.filter(source =>
      this.selectedSourceIds.includes(source.pid)
    );
    
    if (selectedSources.length > 0) {
      this.uploadForm.datasource = selectedSources.map(source => source.sceneName).join(' & ');
      this.selectSourceDialogVisible1 = false;
    } else {
      this.$message.warning('请选择至少一个数据源');
    }
    this.resetSelection();
  },
    cancelSelection1() {
      this.selectSourceDialogVisible1 = false;
      this.sourceSearchQuery1='';
      this.selectedSourceId = null;
      this.resetSelection();
    },
    handleSelectionChange(val) {
      // 更新选中的 ID 列表
      console.log('Selection changed:', val);
      this.selectedSourceId1 = val.map(item => item.sceneName);
      console.log(selectedSourceId1);
    },


    async fetchscenes() {
      try {
        const response = await fetch('/api/systemtable/api/selectAllScenes');  // 替换为你的接口地址
        if (!response.ok) {
          throw new Error('Failed to fetch scenes');
        }
        const jsonData = await response.json();
        console.log('Fetched scenes data:', jsonData);
        if (Array.isArray(jsonData)) {
          this.scenes = jsonData;
          this.filteredSources1=this.scenes
          this.paginateResources1();
        } else {
          console.error('Expected an array, but got:', typeof jsonData);
        }
      } catch (error) {
        console.error('Error fetching scenes:', error);
      }
    },
    async searchResource2() {
      const fields = ['sceneName', 'sceneType', 'sceneDescription'];
      const uniqueResults = new Set();
      const jsonRegex = /<div>\s*({.*?})\s*<\/div>/g;

      try {
        for (const field of fields) {
          const url = `/api/textquery/fuzzySearch?indexName=scenario_list&fieldName=${field}&searchTerm=${this.sourceSearchQuery1}&fuzziness=1`;

          const response = await fetch(url, {
            method: 'POST',
          });

          if (!response.ok) {
            throw new Error(`Failed to fetch search results for field: ${field}`);
          }

          const textResponse = await response.text();
          let match;
          while ((match = jsonRegex.exec(textResponse)) !== null) {
            try {
              const jsonObject = JSON.parse(match[1]);
              uniqueResults.add(JSON.stringify(jsonObject));
            } catch (err) {
              console.error("Error parsing JSON:", err);
            }
          }
        }

        this.filteredSources1 = Array.from(uniqueResults).map(item => JSON.parse(item));
        console.log(this.scenes);
        this.paginateResources1(); // 更新分页后的数据
      } catch (error) {
        console.error('Error fetching search results:', error);
      }
    },



    confirmSelection() {
  const selectedSources = this.filteredSources.filter(source => 
    this.selectedSourceIds.includes(source.pid)
  );
  if (selectedSources.length > 0) {
    this.uploadForm.datasource = selectedSources.map(source => source.name).join('&');
    this.selectSourceDialogVisible = false;
  } else {
    this.$message.warning('请选择一个数据源');
  }
  this.resetSelection();
},

    async fetchResources() {
      try {
        const response = await fetch('/api/systemtable/api/selectAllData');  // 替换为你的接口地址
        if (!response.ok) {
          throw new Error('Failed to fetch resources');
        }

        const textData = await response.text();  // 以纯文本形式获取数据
        console.log('Original response:', textData);  // 打印原始响应

        // 修正数据格式，将其包裹为一个数组
        let formattedData = textData.trim();

        // 移除末尾的分号
        if (formattedData.endsWith(';')) {
          formattedData = formattedData.slice(0, -1);
        }

        // 包裹在数组中
        formattedData = `[${formattedData}]`;

        // 解析为 JSON 数组
        const data = JSON.parse(formattedData);

        // 确保解析成功并是数组
        if (Array.isArray(data)) {
          this.resources = data;
          this.filteredSources = this.resources; // 初始化为所有资源
          this.paginateResources();  // 初始化分页
        } else {
          console.error('Expected an array, but got:', typeof data);
        }
      } catch (error) {
        console.error('Error fetching resources:', error);
      }
    },
    async searchResource1() {
      const fields = ['name', 'type', 'subCategory', 'field', 'description'];
      const uniqueResults = new Set();
      const jsonRegex = /<div>\s*({.*?})\s*<\/div>/g; // 正则表达式匹配 div 中的 JSON 字符串

      try {
        for (const field of fields) {
          const url = `/api/textquery/fuzzySearch?indexName=resource_list&fieldName=${field}&searchTerm=${this.sourceSearchQuery}&fuzziness=1`;

          const response = await fetch(url, {
            method: 'POST',
          });

          if (!response.ok) {
            throw new Error(`Failed to fetch search results for field: ${field}`);
          }

          const textResponse = await response.text();
          console.log(textResponse)
          console.log(1)
          // 使用正则表达式提取 JSON 字符串
          let match;
          while ((match = jsonRegex.exec(textResponse)) !== null) {
            try {
              const jsonObject = JSON.parse(match[1]);
              uniqueResults.add(JSON.stringify(jsonObject)); // 将 JSON 对象序列化后加入 Set
              console.log(uniqueResults);
              console.log(2)
            } catch (err) {
              console.error("Error parsing JSON:", err);
            }
          }
        }

        // 将去重后的结果转化为数组并存储到 filteredSources 中
        this.filteredSources = Array.from(uniqueResults).map(item => JSON.parse(item));
        
        // 重置当前页为第一页
        this.currentPage2 = 1;

        // 更新分页后的数据
        this.paginateResources();
      } catch (error) {
        console.error('Error fetching search results:', error);
      }
    },
    resetUploadForm() {
      this.uploadForm = {
        pid:'',
        fileType: '',
        serviceName: '',
        serviceType: '',
        serviceDescription: '',
        user: '',
        date: '',
        shareState: '',
        datasource: '' // 重置数据源字段
      };
    },
    
    
    submitForm() {
      if (this.uploadForm.serviceDescription&&this.uploadForm.serviceName&&this.uploadForm.serviceType&&this.uploadForm.shareState&&this.uploadForm.datasource) {
        
          // 处理文件上传逻辑
          this.sendPostRequest();
          this.resetUploadForm();
        
      } else {
        this.$message.error('请完整填写数据');
      }
      console.log('表单数据:', this.uploadForm);
      this.uploadDialogVisible = false; // 关闭发布服务弹窗
      this.uploadDialogVisible1 = false;
    },


    async sendPostRequest() {


// 提取文件名和格式
const name1 = this.uploadForm.serviceName;
const type1 = this.uploadForm.serviceType;
  const description1 = this.uploadForm.serviceDescription;
  const user1=this.username;
  const date1=this.getCurrentTime();
  const date2=new Date(date1.replace(' ', 'T'));
  const  sharestate1=this.uploadForm.shareState;
  const datasource1=this.uploadForm.datasource;
  const Pid = generatePID();





// 构建要发送的表单数据
const jsonData = {
  "indexName": 'service_list',
  "docId": Pid,
  "jsonString": {
    "serviceName": this.resources.length + 1,
    "serviceType": this.uploadForm.fileType,
    "serviceDescription": this.uploadForm.subCategory,
    "user": user1,
    "date": date2,
    "shareState": sharestate1,
    "datasource": datasource1
  }
};



try {
  // 使用 fetch 发送 POST 请求
  const response = await fetch('/api/textquery/insertDoc', {
    method: 'POST',
    headers: {  
      'Content-Type': 'application/json' // 设置为 JSON 格式
    },
    body: JSON.stringify(jsonData) // 发送原始 JSON 数据
  });

  // 处理响应
  if (response.ok) {
    const responseData = await response.text(); // 假设服务器返回纯文本响应
    console.log('Response:', responseData);

    // 检查响应中是否包含 "Index:", "ID:", "Version:"
    if (responseData.includes('Index:') && responseData.includes('ID:') && responseData.includes('Version:')) {
      console.log('服务器上传成功');
      try {
 
 // 构造 URL，包含查询参数
 const url = `/api/systemtable/api/insertService?pid=${Pid}&serviceName=${name1}&serviceType=${type1}&serviceDescription=${description1}&datasource=${datasource1}&user=${user1}&date=${date1}&shareState=${sharestate1}`;

 // 发送 GET 请求
 const response = await fetch(url, {
   method: 'GET'
 });

 // 处理响应
 if (response.ok) {
   const responseData = await response.text(); // 假设服务器返回纯文本响应
   console.log('Response:', responseData);

   // 根据响应内容进行不同处理
   if (responseData === 'Service added successfully.') {
     console.log('数据库上传成功');
     alert('上传成功');
     // 处理成功情况，例如显示提示或更新界面
   } else {
     console.log('数据库上传失败:', responseData);
     alert('上传失败');
     // 处理失败情况
   }
 } else {
   console.error('请求失败，状态码:', response.status);
   alert('上传失败');
 }
} catch (error) {
 console.error('请求错误:', error);
}
    } else {
      console.log('无法解析响应:', responseData);
    }
  } else {
    console.error('服务器请求失败，状态码:', response.status);
    alert('服务器请求失败，状态码: ' + response.status);
  }
} catch (error) {
  console.error('请求错误:', error);
}



this.refreshData();
},

    getCurrentTime() {
      const now = new Date();
  const year = now.getFullYear();
  const month = (now.getMonth() + 1).toString().padStart(2, '0'); // 月份从0开始，所以要加1
  const day = now.getDate().toString().padStart(2, '0');
  const hours = now.getHours().toString().padStart(2, '0');
  const minutes = now.getMinutes().toString().padStart(2, '0');
  const seconds = now.getSeconds().toString().padStart(2, '0');
  
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`; 
    },
    // 更新时间的方法
    updateCurrentTime() {
      this.currentTime = this.getCurrentTime();
    },
  
    urlResource(row) {
    this.serviceUrl = row.url; // 设置弹窗显示的 URL
    this.urlDialogVisible = true;
  },
  
  // 复制 WMS URL 到剪贴板
  copyWMSUrl() {
    this.copyToClipboard(this.serviceUrl); // 实际复制的 URL，依据实际情况设置
    this.$message.success('WMS URL 已复制到剪贴板');
  },

  // 复制 URL 到剪贴板
  copyUrl() {
    this.copyToClipboard(this.serviceUrl);
    this.$message.success('URL 已复制到剪贴板');
  },

  // 通用复制到剪贴板的函数
  copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
  },

  // 重置 URL 弹窗状态
  resetUrlDialog() {
    this.urlDialogVisible = false;
    this.serviceUrl = '';
  },
  deleteResource(row) {
    this.resourceToDelete = row;
    this.deleteDialogVisible = true;
  },
  async confirmDelete(service) {
  try {
    await this.$confirm('确认删除该任务?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });

    const service1 = service;  // 获取传入的 service

    // 先删除另一个数据库中的数据 (使用 POST 请求)
    const esResponse = await fetch(`/api/textquery/deleteDoc?indexName=service_list&docId=${service1.pid}`, {
      method: 'POST',
    });

    const esResponseData = await esResponse.text();
    if (esResponseData.includes('Document deleted with ID:')) {
      console.log('es服务器删除成功');

      // 继续删除主数据库中的数据
      const dbResponse = await fetch(`/api/systemtable/api/deleteService?pid=${service1.pid}`, {
        method: 'GET'
      });

      const dbResponseData = await dbResponse.text();
      if (dbResponseData.includes('deleted successfully.')) {
        console.log('数据库删除成功');
        alert('删除成功');
        // 从本地资源列表中删除该资源
        this.services = this.services.filter(item => item !== service1);
      } else {
        console.error('数据库删除失败:', dbResponseData);
        alert('删除失败');
      }
    } else {
      console.error('es服务器删除失败:', esResponseData);
      alert('删除失败');
    }
  } catch (error) {
    console.error('请求错误:', error);

  } finally {
    // 关闭删除确认对话框
    this.deleteConfirmVisible = false;
    // 刷新数据
    setTimeout(() => {
      this.refreshData();
    }, 1000);
  }
},

  resetDeleteDialog() {
    this.deleteDialogVisible = false;
    this.resourceToDelete = null;
  },
    showSingleLayerModal() {
      this.singleLayerDialogVisible = true;
    },
    showMultipleLayersModal() {
      this.multipleLayersDialogVisible = true;
    },
  
  
    handleSingleLayerSizeChange(size) {
      this.singleLayerPageSize = size;
    },
    handleSingleLayerCurrentChange(page) {
      this.singleLayerCurrentPage = page;
    },
    handleMultipleLayersSizeChange(size) {
      this.multipleLayersPageSize = size;
    },
    handleMultipleLayersCurrentChange(page) {
      this.multipleLayersCurrentPage = page;
    },
    handleSingleLayerSelectionChange(selection) {
      this.selectedSingleLayers = selection;
    },
    handleMultipleLayersSelectionChange(selection) {
      this.selectedMultipleLayers = selection;
    },
    confirmSingleLayerSelection() {
      if (this.selectedSingleLayers.length > 0) {
        // Handle single layer selection confirmation
        this.serviceSettingsDialogVisible = true;
      }
    },
    confirmMultipleLayersSelection() {
      if (this.selectedMultipleLayers.length > 0) {
        // Handle multiple layers selection confirmation
        this.serviceSettingsDialogVisible = true;
      }
    },
    resetSingleLayerForm() {
      this.singleLayerSearchQuery = '';
      this.singleLayerCurrentPage = 1;
      this.selectedSingleLayers = []; // Reset selection
      this.singleLayerDialogVisible = false;
    },
    resetMultipleLayersForm() {
      this.multipleLayersSearchQuery = '';
      this.multipleLayersCurrentPage = 1;
      this.selectedMultipleLayers = []; // Reset selection
      this.multipleLayersDialogVisible = false;
    },
    resetServiceSettingsForm() {
      this.serviceSettingsForm = {
        serviceType: '',
        serviceName: '',
        serviceDescription: ''
      };
      this.serviceSettingsDialogVisible = false;
    },
    confirmServiceSettings() {
      // Handle service settings confirmation
      this.resetServiceSettingsForm();
    },
    resetSelection() {
    this.$nextTick(() => {
      if (this.$refs.dataTable) {
        this.$refs.dataTable.clearSelection();
      }
    });
  },
  resetSelection1() {
    this.selectedSourceIds = []; // 重置选中的ID数组
  },
    logout() {
      localStorage.removeItem('username');
localStorage.removeItem('region');   

      this.$router.push('/system');
    },
    handleSizeChange1(newSize) {
      this.pageSize1 = newSize;
      this.currentPage1 = 1; // 重置到第一页
      this.paginateResources1();
    },
    handlePageChange1(newPage) {
      this.currentPage1 = newPage;
      this.paginateResources1();
    },
    handleSizeChange2(newSize) {
      this.pageSize2 = newSize;
      this.currentPage2 = 1; // 重置到第一页
      this.paginateResources();
    },
    handlePageChange2(newPage) {
      this.currentPage2 = newPage;
      this.paginateResources();
    }
  },
  mounted() {
    this.refreshData(); // 加载数据源
  }
};

</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #f8f5f5;
  padding: 10px;
  border-bottom: 1px solid #e7e7e7;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-center .el-menu-demo .el-menu-item a {
  text-decoration: none; /* 确保没有下划线 */
  color: inherit; /* 确保文字颜色继承自父元素 */
}

.navbar-center .el-menu-demo .el-menu-item a:hover {
  text-decoration: none; /* 鼠标悬停时移除下划线 */
}

.router-link-active{
  color: #ffd04b; /* 激活时文字颜色 */
  border-bottom: #ffd04b;
}

.navbar-left .logo {
  font-size: 16px;
  font-weight: bold;
  color: #1d1818; /* 灰色文字 */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2); /* 文字虚化效果 */ 
}

.navbar-right .user-info {
  margin-right: 10px;
}

.el-menu-demo {
  flex: 1;
  display: flex;
  justify-content: center;
}

.user-info {
  margin-right: 10px;
}

.content {
  margin-top: 10px;
  padding: 10px;
}

.custom-input {
  width: 75%;
}

.dialog-footer-content {
  text-align: right;
}

.el-button {
  margin-right: 10px;
}

.search-box {
  margin-bottom: 20px;
}

.actions {
  display: flex;
  flex-direction: column;
}

.action-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 5px;
}

.compact-button {
  padding: 0 8px;
}

.dialog-footer {
  text-align: right;
}
.button-container {
  display: flex; /* 使用 flex 布局 */
  justify-content: flex-start; /* 按钮左对齐 */
  gap: 10px; /* 按钮之间的间距 */
  margin: 10px 0; /* 顶部和底部的外边距 */
  margin-left: 150px;
}
.hidden-radio .el-radio__label {
  display: none; /* 隐藏标签文字 */
}

.hidden-radio .el-radio__input {
  width: 20px; /* 调整单选框的大小 */
  height: 20px;
  margin: 0; /* 移除默认的 margin */
  display: flex; /* 确保 radio 输入框正确显示 */
  align-items: center; /* 垂直居中对齐 */
}

.hidden-radio .el-radio__inner {
  border: none; /* 移除边框 */
  background: none; /* 去除背景 */
}

.hidden-radio .el-radio__inner:checked {
  background: #409EFF; /* 选中状态下背景颜色 */
  border: 1px solid #409EFF; /* 选中状态下边框颜色 */
}

.hidden-radio .el-radio__inner:disabled {
  background: #f5f7fa; /* 禁用状态下背景颜色 */
  border: 1px solid #dcdfe6; /* 禁用状态下边框颜色 */
}

.custom-button {
  width: 105px; /* 设置按钮的宽度，调整为你需要的宽度 */
  padding: 0 10px; /* 调整按钮内边距，使其看起来更紧凑 */
  height: 40px;
  margin-left: 90px;
  margin-bottom: 10px;
}
.hidden-checkbox {
  position: relative;
  display: inline-block;
}

.hidden-checkbox .el-checkbox__input {
  display: inline-block;
}

.hidden-label {
  display: none; /* 隐藏 label */
}
</style>