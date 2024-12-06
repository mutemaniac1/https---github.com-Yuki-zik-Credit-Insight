<template>
  <div>
    <el-row class="navbar" type="flex" justify="space-between" align="middle">
  <el-col :span="7" class="navbar-left">
    <span class="logo">城市存量空间数据场景化<br>集成与一体化管理系统</span>
  </el-col>
  <el-col :span="9" class="navbar-center">
    <el-menu mode="horizontal" default-active="2" class="el-menu-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
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
          <h1>数据资源列表</h1>

          <el-row class="search-box">
            <el-col :span="8">
              <el-button type="primary" @click="showUploadModal">文件上传数据</el-button>
            </el-col>
            <el-col :span="8">
              <el-input v-model="searchQuery" placeholder="搜索资源..."></el-input>
            </el-col>
            <el-col :span="8">
              <el-button type="primary" @click="searchResource">搜索</el-button>
              <el-button @click="refreshData">刷新</el-button>
            </el-col>
          </el-row>

          <el-table :data="paginatedResources" style="width: calc(100% - 40px); margin: 0 20px;">
            <el-table-column prop="id" label="序号"></el-table-column>
            <el-table-column prop="type" label="数据类别"></el-table-column>
            <el-table-column prop="name" label="数据名称"></el-table-column>
            <el-table-column prop="isspatial" label="是否为空间数据" :formatter="formatIsSpatial">
</el-table-column>

            <el-table-column prop="format" label="数据格式"></el-table-column>
            <el-table-column prop="field" label="字段"></el-table-column>
            <el-table-column prop="coordinate" label="数据坐标系"></el-table-column>
            <el-table-column prop="description" label="数据使用描述"></el-table-column>
            <el-table-column label="操作">
        <template slot-scope="scope">
          <div class="actions">
            <div class="button-group">
              <el-button size="mini" class="action-button" @click="editResource(scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" class="action-button" @click="deleteResource(scope.row)">删除</el-button>
            </div>
            <div class="button-group">
              <el-button size="mini" type="primary" class="action-button" @click="downloadResource(scope.row)">下载</el-button>
              <el-button 
                size="mini" 
                type="success" 
                class="action-button" 
                :disabled="!scope.row.isUploaded" 
                @click="importToDatabase(scope.row)">
                入库
              </el-button>
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
          :total="filteredResources.length">
        </el-pagination>
      </div>
    </el-card>

    <!-- 上传弹窗 -->
    <el-dialog
  title="文件上传数据"
  :visible.sync="uploadDialogVisible"
  width="40%"
  @close="resetUploadForm">
  <el-form :model="uploadForm" label-width="130px" class="elform">
    <el-form-item label="选择文件">
  <el-upload
ref="upload"
    class="upload-demo"
    :show-file-list="false"
    :before-upload="beforeupload"
    :on-change="handleFileChange"
    :auto-upload="false"
    multiple
    accept=".csv,.json,.xlsx,.xls,.mdb,.dbf,.txt,.doc,.pdf,.xml,.h5,.npy,.onnx,.pth,.db,.dump,.ttl,.owl,.tiff,.jp2,.img,.grib,.shp,.dxf,.gdb,.geojson,.hdf5,.nc,.obj,.fbx,.max,.ply,.las,.xyz,.png,.jpg,.mvt,.uasset,.osgb,.zip,.shx,.sbn,.prj"
  >
    <el-button slot="trigger" @click="clearPreviousFiles"  size="small" style="margin-left: -80px;">选择文件</el-button>
  </el-upload>

  <!-- 显示单个文件或多个文件 -->
  <div v-if="selectedFile" class="selected-file" style="margin-left: -80px;">
    <el-tag>{{ selectedFile.name }}</el-tag>
  </div>
  <div v-else-if="selectedFiles" class="selected-files" style="margin-left: -80px;">
    <el-tag v-for="(file, index) in limitedFiles" :key="index" class="selected-file">
      {{ file.name }}
    </el-tag>
    <span v-if="selectedFiles.length > 2">... ({{ selectedFiles.length }} files selected)</span>
  </div>
</el-form-item>

     <!-- 上传弹窗 
    <el-form-item label="选择文件">
      <el-upload
        class="upload-demo"
        :show-file-list="false"
        :before-upload="beforeUpload"
        :on-change="handleFileChange"
        multiple
        accept=".csv,.json,.xlsx,.xls,.mdb,.dbf,.txt,.doc,.pdf,.xml,.h5,.npy,.onnx,.pth,.db,.dump,.ttl,.owl,.tiff,.jp2,.img,.grib,.shp,.dxf,.gdb,.geojson,.hdf5,.nc,.obj,.fbx,.max,.ply,.las,.xyz,.png,.jpg,.mvt,.uasset,.osgb"
        >
        <el-button slot="trigger" size="small" style="margin-left: -80px;">文件</el-button>
      </el-upload>
      <el-tag v-if="selectedFile" class="selected-file" style="margin-left: -80px;">{{ selectedFile.name }}</el-tag>
    </el-form-item>-->
    <el-form-item label="数据分类">
    <el-select v-model="uploadForm.fileType" placeholder="请选择数据分类" class="custom-input" @change="handleFileTypeChange">
      <el-option label="基础时空数据" value="基础时空数据"></el-option>
      <el-option label="公共专题数据" value="公共专题数据"></el-option>
      <el-option label="城市感知数据" value="城市感知数据"></el-option>
      <el-option label="课题成果数据" value="课题成果数据"></el-option>
    </el-select>
  </el-form-item> 

  <el-form-item label="具体类别">
    <el-select v-model="uploadForm.subCategory" placeholder="请选择具体类别" :disabled="!uploadForm.fileType" class="custom-input">
      <el-option
        v-for="option in subCategoryOptions"
        :key="option.value"
        :label="option.label"
        :value="option.value">
      </el-option>
    </el-select>
  </el-form-item>
   
    <el-form-item label="是否空间数据">
  <el-radio-group v-model="uploadForm.isSpatialData" class="custom-input" @change="judge">

    <el-radio :label="'是'" value="是">是</el-radio>
    <el-radio :label="'否'" value="否">否</el-radio>
  </el-radio-group>
</el-form-item>


    <el-form-item label="数据描述">
      <el-input type="textarea" v-model="uploadForm.resourceDescription" class="custom-input"></el-input>
    </el-form-item>
    <!-- 新增所属空间范围 -->
   <el-form-item label="所属空间范围">
    <div style="display: flex; align-items: center;">
      <el-cascader
        v-model="uploadForm.spatialRange"
        :options="spatialOptions"
        placeholder="请选择所属空间范围"
        class="custom-input"
        :show-all-levels="false"
        :props="cascaderProps"
        @change="handleCascaderChange"
      >
      </el-cascader>
      <el-button 
        type="primary" 
        size="mini" 
        @click="chooseSpatialFile"
        style="margin-left: 10px;">
        {{ '选择范围' }}
      </el-button>
      
    </div>
    <div v-if="selectedFiles1.length > 0" style="margin-left: 10px;">
        已选择文件：
        <ul>
          <li v-for="(file, index) in selectedFiles1" :key="index">
            {{ file.name }}
          </li>
        </ul>
      </div>
  </el-form-item>
      
    <div class="dialog-footer-content">
      <el-button type="primary" @click="confirmUpload">确定</el-button>
      <el-button @click="resetUploadForm">取消</el-button>
    </div>
  </el-form>
</el-dialog>

    <!-- 删除确认弹窗 -->
    <el-dialog
      title="删除确认"
      :visible.sync="deleteConfirmDialogVisible"
      width="30%"
      @close="resetDeleteConfirm">
      <p>是否删除该数据盗源? 删除之后将无法恢复，该数据源下的所有图层服务也将会被删除!</p>
      <div class="dialog-footer-content">
        <el-button type="danger" @click="confirmDelete">删除</el-button>
        <el-button @click="cancelDelete">取消</el-button>
      </div>
    </el-dialog>

    <!-- 选择不符弹窗 -->
    <el-dialog
      title="提示"
      :visible.sync="mismatchDialogVisible"
      width="30%">
      <p>您的选择与常规不相符，要坚持您的选择吗？</p>
      <div class="dialog-footer-content">
        <el-button type="primary" @click="confirmMismatch">确定</el-button>
        <el-button @click="cancelMismatch">取消</el-button>
      </div>
    </el-dialog>

    <!-- 上传进度弹窗 -->
    <el-dialog
  title="上传文件"
  :visible.sync="uploadProgressVisible"
  width="30%"
  :before-close="handleCloseProgressDialog"
>
  <el-progress :percentage="uploadProgress" :text-inside="true" :stroke-width="20"></el-progress>
  <div v-if="uploadProgress === 100" style="text-align: center; margin-top: 20px;">
    <span>上传成功</span>
  </div>
  <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="handleCloseProgressDialog">确定</el-button>
  </span>
</el-dialog>

<el-dialog
      title="编辑数据资源"
      :visible.sync="editDialogVisible"
      width="40%"
      @close="resetEditForm">
      <el-form :model="editForm" label-width="130px">
        <el-form-item label="数据类别">
          <el-select v-model="editForm.type" placeholder="请选择数据类别" @change="handleFileTypeChange">
            <el-option label="基础时空数据" value="基础时空数据"></el-option>
            <el-option label="公共专题数据" value="公共专题数据"></el-option>
            <el-option label="城市感知数据" value="城市感知数据"></el-option>
            <el-option label="课题成果数据" value="课题成果数据"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="具体子类">
          <el-select v-model="editForm.subCategory" placeholder="请选择具体子类">
            <el-option
              v-for="option in subCategoryOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据描述">
          <el-input type="textarea" v-model="editForm.description"></el-input>
        </el-form-item>

        <div class="dialog-footer">
          
          <el-button type="primary" @click="confirmEdit">确定</el-button>
          <el-button @click="resetEditForm">取消</el-button>
        </div>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>

import { spatialOptions } from './spatialOptions.js';
import { generatePID } from './pidGenerator';

export default {
  data() {
    return {
      uploadComplete: false, 
      selectedFiles1: [],
      selectedFiles: [], // 存储选中的文件数组
      spatialOptions: [], // 级联选择器的选项
      cascaderProps: {
        value: 'value',
        label: 'label',
        children: 'children'
      },// 级联选择器的属性
      editDialogVisible: false,
      editForm: {
        pid:'',
        type: '',
        subCategory: '',
        description: '',
        state:'',
        isUploaded:''
      },
      userSelectedSpatialData: null,
      username: localStorage.getItem('username'),
      region : localStorage.getItem('region'), 
      resources: [],  // 存储从服务器获取的数据
    filteredResources: [], // 用于存储搜索过滤后的数据
    paginatedResources: [], // 分页显示的数据
      searchQuery: '',
      currentPage: 1,
      pageSize: 5,
      uploadDialogVisible: false,
      deleteConfirmDialogVisible: false,
      mismatchDialogVisible: false,
      spatialFileName: '',
      uploadForm: {
        id:null,
        fileType: '',
        pid:'',
        size:null,
        subCategory: '',
        resourceName: '',
        isSpatialData: '',
        fields: '',
        coordinateSystem: '',
        resourceDescription: '',
        file: null,
        state:'',
        spatialRange: [], // 新增字段
        spatialFile: null,
        isUploaded:false,
      },
      subCategoryOptions: [],
      selectedFile: null,
      deleteTarget: null,
      uploadProgressVisible: false, // 控制进度条弹窗的显示
    uploadProgress: 0 ,// 上传进度
    spatialOptions,
    cascaderProps: {
        multiple: true,
        checkStrictly: true,
        emitPath: false,
      },
    };
  },
  
  mounted() {
  this.fetchResources();  // 正确的写法
},
computed: {
    // 只显示前两个文件
    limitedFiles() {
      return this.selectedFiles.slice(0, 2);
      
    }
  },
  methods: {
    formatIsSpatial(row, column, cellValue) {
    return cellValue ? '是' : '否';  // 如果是 true，显示 "是"，否则显示 "否"
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
      this.filteredResources = this.resources;
      this.paginateResources();  // 初始化分页
    } else {
      console.error('Expected an array, but got:', typeof data);
    }
  } catch (error) {
    console.error('Error fetching resources:', error);
  }
},



  paginateResources() {
    const start = (this.currentPage - 1) * this.pageSize;
    const end = this.currentPage * this.pageSize;
    this.paginatedResources = this.filteredResources.slice(start, end);
  },
  
  async searchResource() {
  const fields = ['name', 'type', 'subCategory', 'field', 'description'];
  const uniqueResults = new Set();
  const jsonRegex = /<div>\s*({.*?})\s*<\/div>/g; // 正则表达式匹配 div 中的 JSON 字符串

  try {
    for (const field of fields) {
      const url = `/api/textquery/fuzzySearch?indexName=resource_list&fieldName=${field}&searchTerm=${this.searchQuery}&fuzziness=1`;

      const response = await fetch(url, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch search results for field: ${field}`);
      }

      const textResponse = await response.text();

      // 使用正则表达式提取 JSON 字符串
      let match;
      while ((match = jsonRegex.exec(textResponse)) !== null) {
        try {
          const jsonObject = JSON.parse(match[1]);
          uniqueResults.add(JSON.stringify(jsonObject)); // 将 JSON 对象序列化后加入 Set
        } catch (err) {
          console.error("Error parsing JSON:", err);
        }
      }
    }

    // 将去重后的结果转化为数组并存储到 filteredResources 中
    this.filteredResources = Array.from(uniqueResults).map(item => JSON.parse(item));
    
    this.paginateResources(); // 更新分页后的数据
  } catch (error) {
    console.error('Error fetching search results:', error);
  }
},


  
  handleSizeChange(newSize) {
    this.pageSize = newSize;
    this.paginateResources();
  },
  
  handleCurrentChange(newPage) {
    this.currentPage = newPage;
    this.paginateResources();
  },
  
  refreshData() {
    this.fetchResources();  // 重新从服务器获取数据
    console.log(this.region);
  },
  editResource(resource) {
  // 打开编辑弹窗，并初始化表单数据
  this.editForm = {
    pid: resource.pid, // 假设 ID 是唯一标识符，映射到 PID
    type: resource.type,
    subCategory: resource.subCategory,
    description: resource.description,
    state:resource.state,
    isUploaded:resource.isUploaded
  };
  this.handleFileTypeChange(resource.type);
  this.editDialogVisible = true;
},

async confirmEdit() {
  const pid1=this.editForm.pid;
  const type1=this.editForm.type;
  const subCategory1=this.editForm.subCategory;
  const description1=this.editForm.description;
  const state1=this.editForm.state;
  const isUploaded2=this.editForm.isUploaded;

  try {
    // 发送 POST 请求到服务器更新数据
    const jsonData = {
      indexName: 'resource_list', // 设置 indexName
      docId: this.editForm.pid,    // 设置 docId
      jsonString: {
        type: this.editForm.type,
        subCategory: this.editForm.subCategory,
        description: this.editForm.description
      }
    };

    // 发送 POST 请求到 ES 服务器
    
    const serverResponse = await fetch('/api/textquery/updateDoc', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // 告知服务器数据格式
      },
      body: JSON.stringify(jsonData)
    });

    const serverData = await serverResponse.text();
    console.log('Server response:', serverData);

    // 检查响应是否包含特定字样
    if (serverData.includes('Index: resource_list') && serverData.includes('ID:')) {
      console.log('服务器更新成功');
      
      // 如果服务器返回更新成功，则继续更新数据库
      const dbResponse = await fetch(
        `/api/systemtable/api/updateData?pid=${parseInt(pid1)}&type=${type1}&subCategory=${subCategory1}&description=${description1}&state=${state1}&isUploaded=${isUploaded2}`,
        {
          method: 'GET'
        }
      );

      if (dbResponse.ok) {
        const dbData = await dbResponse.text(); // 数据库返回纯文本
        console.log('Database response:', dbData);

        if (dbData.includes('updated successfully')) {
          console.log('编辑成功');
          alert('编辑成功')
          // 处理成功的逻辑，例如刷新数据或提示
        } else {
          console.error('数据库更新失败:', dbData);
          alert('编辑失败')
          // 处理失败逻辑
        }
      } else {
        console.error('数据库请求失败，状态码:', dbResponse.status);
      }
    } else {
      console.error('服务器更新失败，状态码:', serverResponse.status);
      alert('编辑失败')
    }
  } catch (error) {
    console.error('请求错误:', error);
  }
    setTimeout(() => {
      this.refreshData();
    }, 1000); 
  // 关闭编辑弹窗
  this.editDialogVisible = false;
},

    resetEditForm() {
      this.editDialogVisible = false;
      this.editForm = {
        pid:'',
        type: '',
        subCategory: '',
        description: '',
        state:'',
        isUploaded:''
      };
    },
    handleCascaderChange(value) {
      // 重置所有子类和子类的子类的禁用状态
      this.spatialOptions.forEach(mainCategory => {
        mainCategory.children.forEach(subCategory => {
          subCategory.disabled = true;
          if (subCategory.children) {
            subCategory.children.forEach(grandChild => {
              grandChild.disabled = true;
            });
          }
        });
      });

      // 启用已选择的主类的子类
      value.forEach(selectedValue => {
        const selectedMainCategory = this.spatialOptions.find(
          option => option.value === selectedValue
        );
        if (selectedMainCategory) {
          selectedMainCategory.children.forEach(child => {
            child.disabled = false;
          });
        }

        // 启用已选择的子类的子类
        this.spatialOptions.forEach(mainCategory => {
          mainCategory.children.forEach(subCategory => {
            if (value.includes(subCategory.value)) {
              if (subCategory.children) {
                subCategory.children.forEach(grandChild => {
                  grandChild.disabled = false;
                });
              }
            }
          });
        });
      });
    },
    handleFileTypeChange(value) {
      const subCategories = {
        "基础时空数据": [
          { label: "基础地理数据", value: "基础地理数据" },
          { label: "三维模型数据", value: "三维模型数据" },
          { label: "地理切片数据", value: "地理切片数据" }
        ],
        "公共专题数据": [
          { label: "国土空间数据", value: "国土空间数据" },
          { label: "社会经济数据", value: "社会经济数据" },
          { label: "城市交通数据", value: "城市交通数据" },
          { label: "生态环境数据", value: "生态环境数据" },
          { label: "安全保障数据", value: "安全保障数据" },
          { label: "历史文化数据", value: "历史文化数据" }
        ],
        "城市感知数据": [
          { label: "物联感知数据", value: "物联感知数据" },
          { label: "社会感知数据", value: "社会感知数据" },
          { label: "互联网在线数据", value: "互联网在线数据" }
        ],
        "课题成果数据": [
          { label: "识别成果数据", value: "识别成果数据" },
          { label: "评估成果数据", value: "评估成果数据" },
          { label: "优化成果数据", value: "优化成果数据" }
        ]
      };
      this.subCategoryOptions = subCategories[value] || [];
      this.uploadForm.subCategory = ''; // 重置子类别选择
    },
    handleFileChange(file, fileList) {

  if (fileList.length === 1) {
    // 单个文件的处理逻辑
    this.selectedFile = file.raw;
    this.selectedFiles = [];  // 清空多文件选择状态
    const spatialDataExtensions = [
      'tiff', 'jp2', 'img', 'grib', 'shp', 'dxf', 'gdb', 'geojson', 'hdf5',
      'nc', 'obj', 'fbx', 'max', 'ply', 'las', 'xyz', 'png', 'jpg', 'mvt',
      'uasset', 'osgb', 'json','zip'
    ];
    const nonSpatialDataExtensions = [
      'xls', 'csv', 'mdb', 'dbf', 'txt', 'doc', 'pdf', 'xml', 'h5', 'npy',
      'onnx', 'pth', 'db', 'dump', 'ttl', 'owl'
    ];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const isSpatialDataFile = spatialDataExtensions.includes(fileExtension);
    const isNonSpatialDataFile = nonSpatialDataExtensions.includes(fileExtension);

    if (
      (this.uploadForm.isSpatialData === '是' && !isSpatialDataFile) ||
      (this.uploadForm.isSpatialData === '否' && !isNonSpatialDataFile)
    ) {
      this.mismatchDialogVisible = true;
    } else {
      this.userSelectedSpatialData = this.uploadForm.isSpatialData;
    }
    
  } else {
    // 多个文件的处理逻辑，直接认定为空间数据
    this.selectedFiles = fileList;
    console.log(fileList)
      this.selectedFile = null; //清除单个文件的选择
    const isSpatialDataFile = true;
    const isNonSpatialDataFile = false;
    if (
      (this.uploadForm.isSpatialData === '是' && !isSpatialDataFile) ||
      (this.uploadForm.isSpatialData === '否' && !isNonSpatialDataFile)
    ) {
      this.mismatchDialogVisible = true;
    } else {
      this.userSelectedSpatialData = this.uploadForm.isSpatialData;
    }
   
  }
  
},

judge() {
  // 针对单个文件的判断逻辑
  if (this.selectedFile) {
    const file = this.selectedFile;

    const spatialDataExtensions = [
      'tiff', 'jp2', 'img', 'grib', 'shp', 'dxf', 'gdb', 'geojson', 'hdf5',
      'nc', 'obj', 'fbx', 'max', 'ply', 'las', 'xyz', 'png', 'jpg', 'mvt',
      'uasset', 'osgb', 'json','zip'
    ];
    const nonSpatialDataExtensions = [
      'xls', 'csv', 'mdb', 'dbf', 'txt', 'doc', 'pdf', 'xml', 'h5', 'npy',
      'onnx', 'pth', 'db', 'dump', 'ttl', 'owl'
    ];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const isSpatialDataFile = spatialDataExtensions.includes(fileExtension);
    const isNonSpatialDataFile = nonSpatialDataExtensions.includes(fileExtension);

    if (
      (this.uploadForm.isSpatialData === '是' && !isSpatialDataFile) ||
      (this.uploadForm.isSpatialData === '否' && !isNonSpatialDataFile)
    ) {
      this.mismatchDialogVisible = true;
    } else {
      this.userSelectedSpatialData = this.uploadForm.isSpatialData;
    }
  } else if (this.selectedFiles.length > 1) {
    // 多个文件的处理逻辑，直接认定为空间数据
    const isSpatialDataFile = true;
    const isNonSpatialDataFile = false;
    if (
      (this.uploadForm.isSpatialData === '是' && !isSpatialDataFile) ||
      (this.uploadForm.isSpatialData === '否' && !isNonSpatialDataFile)
    ) {
      this.mismatchDialogVisible = true;
    } else {
      this.userSelectedSpatialData = this.uploadForm.isSpatialData;
    }
  }
},
    confirmMismatch() {
      this.userSelectedSpatialData = this.uploadForm.isSpatialData;
      this.mismatchDialogVisible = false;
    },
    cancelMismatch() {
      this.selectedFile = null;
      this.selectedFiles=[];
      
      this.uploadForm.isSpatialData='';
      this.mismatchDialogVisible = false;
    },
    chooseSpatialFile() {
      const input = document.createElement('input');
      input.type = 'file';
      input.multiple = true; // 允许选择多个文件
      input.accept = '.shp,.shx,.sbx,.sbn,.prj,.dbf,.cpg'; // 允许选择的文件类型

      input.onchange = (event) => {
        const files = Array.from(event.target.files); // 将文件列表转换为数组
        const selectedFiles = [];

        if (files.length > 0) {
          // 使用文件的基本名称来筛选文件
          const baseName = files[0].name.replace(/\.[^/.]+$/, '');

          files.forEach(file => {
            if (file.name.startsWith(baseName)) {
              selectedFiles.push(file);
            }
          });

          console.log(selectedFiles);
          this.selectedFiles1 = selectedFiles; // 存储所有选中的文件
        }
      };

      input.click();
    },
   
  async confirmUpload() {
      if ((this.selectedFile||this.selectedFiles)&&this.uploadForm.fileType&&this.uploadForm.isSpatialData&&this.uploadForm.resourceDescription&&this.uploadForm.subCategory&&this.uploadForm.spatialRange||(this.selectedFile||this.selectedFiles)&&this.uploadForm.fileType&&this.uploadForm.isSpatialData&&this.uploadForm.resourceDescription&&this.uploadForm.subCategory&&this.uploadForm.spatialFile) {
        if (this.userSelectedSpatialData !== this.uploadForm.isSpatialData) { 
          this.$message.error('请选择文件后再上传');
        } else {
          // 处理文件上传逻辑
          
          await this.uploadToServer(); // 上传文件


        
      this.resetUploadForm();
             setTimeout(() => {
      this.refreshData();
    }, 1000); 
        }
      } else {
        this.$message.error('请选择文件后再上传');
      }
    },
    resetUploadForm() {
      this.uploadDialogVisible = false;
      this.uploadForm = {
        pid:'',
        size:null,
        fileType: '',
        subCategory: '',
        resourceName: '',
        isSpatialData: '',
        fields: '',
        coordinateSystem: '',
        resourceDescription: '',
        file:null,
        spatialRange:[],
        spatialFile:null,
        isUploaded:false,
        state:''
      };
      this.selectedFile = null;
      this.selectedFiles=[];
      
      this.selectedFiles1=[];
      this.subCategoryOptions = [];

    },
    beforeupload(file) {
      
      this.selectedFile = null;
    this.selectedFiles = [];
   
      return true;
    },
  
    clearPreviousFiles(){
      this.$refs.upload.clearFiles();
    },
    delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  },
  async uploadToServer() {

    let fileSize = 0;
    const Pid = generatePID();
    this.uploadForm.pid = Pid;
    const formData = new FormData();
    formData.append('fileType', this.uploadForm.fileType);  // 文件类型
    formData.append('userRegion', this.region);  // 用户地区
    formData.append('pid', Pid);
    console.log(Pid);
         
    // 根据文件数量动态添加文件到 formData
      if (this.selectedFiles && this.selectedFiles.length > 0) {
          this.selectedFiles.forEach((file, index) => {
              const key = `file${index + 1}`; // 创建一个新的变量来存储键名
              formData.append(key, file.raw);
              
          });
    } else if (this.selectedFile) {
        formData.append('file1', this.selectedFile);  // 单个文件
    }
    for (const [key, value] of formData) {
        console.log(key, value);
    }
    // 显示上传进度弹窗
    this.uploadProgressVisible = true;
    this.uploadProgress = 0; // 初始化进度条为 0%

    try {
        const response = await fetch('/api/ingestion/upload', {
            method: 'POST',
            body: formData
            
        });
        console.log(formData);
        const text = await response.text();
        console.log('Received text:', text);
        const trimmedText = text.trim();
        console.log('Trimmed text:', trimmedText);

        // 检查响应内容是否包含 "uploaded successfully"
        if (trimmedText.includes("uploaded successfully")) {
            console.log('上传成功:', text);
           
        } else {
            console.error('上传失败:', text);
            this.$message.error('上传失败，请重试');
        }
        await this.delay(1000);
        // 获取所有文件的大小，通过接口查询
        const srResponse = await fetch(`/api/ingestion/upload?pid=${Pid}`, { method: 'GET' });
        const responseData = await srResponse.text();

        // 检查返回的内容是否包含 "File path:"
        if (!responseData.includes('File path:')) {
            console.error('查询失败: 没有找到文件路径信息');
            return; // 如果查询失败，停止执行
        }

        // 解析响应内容，提取文件路径和大小
        const filePathMatches = responseData.split('\n').filter(line => line.includes('File path:'));

        filePathMatches.forEach(line => {
            const pathMatch = line.match(/File path:\s*(.*), Size: (\d+) bytes/);
            if (pathMatch) {
                const fileSize2 = parseInt(pathMatch[2], 10); // 转换文件大小为整数
                fileSize += fileSize2; // 累加文件大小
            }
        });

        // 将总文件大小传给 uploadForm.size
        this.uploadForm.size = fileSize;

    } catch (error) {
        console.error('上传失败:', error.message);
        this.$message.error('上传失败，请重试');
    }

    const pid1=this.uploadForm.pid;
  this.uploadForm.isUploaded = true;
  let spatial = false;
  if (this.uploadForm.isSpatialData === "是") {
    spatial = true;
  };

  // 提取文件名和格式
  let name1 = "", format1 = "";

  if (this.selectedFiles && this.selectedFiles.length > 0) {
    // 查找是否有 .shp 文件
    const shpFile = this.selectedFiles.find(file => file.name.endsWith('.shp'));
    if (shpFile) {
      name1 = shpFile.name.split('.').slice(0, -1).join('.'); // 取 .shp 文件的名称
      format1 = 'shp'; // 格式设为 shp
    }
  } else {
    // 单文件的情况，直接根据文件类型来处理
    if (this.selectedFile.name.endsWith('.zip')) {
      await this.delay(2000);
      // 第一个请求: 上传文件
      console.log(pid1)
      name1 = this.selectedFile.name.split('.').slice(0, -1).join('.');
      const srResponse = await fetch(`/api/ingestion/upload?pid=${pid1}`, { 
        method: 'GET'
      });

      const responseData1 = await srResponse.text();

      // 如果查询失败，直接返回
      if (!responseData1.includes('File path:')) {
        console.error('查询失败:', responseData1);
        this.$message.error('查询失败，请重试');
        return; // 如果查询失败，停止执行
      }

      // 匹配并提取格式
      const formatMatch = responseData1.match(/Format:\s*(\w+)/);
      if (formatMatch) {
        format1 = formatMatch[1].toLowerCase();
      } else {
        console.error('未找到文件格式');
        this.$message.error('未找到文件格式');
        return;
      }
    } else {
      // 单文件的情况，直接提取文件名和格式
      name1 = this.selectedFile.name.split('.').slice(0, -1).join('.');
      format1 = this.selectedFile.name.split('.').pop().toLowerCase();
    }
  }

  console.log('name1:', name1, 'format1:', format1);

  // 如果无法确定文件名和格式，提示用户
  if (!name1 || !format1) {
    console.error('无法确定文件的名称或格式');
    this.$message.error('无法确定文件的名称或格式');
    return;
  }
 /* console.log(pid1);
        console.log(name1);
        console.log(this.uploadForm.fileType);
        console.log(this.uploadForm.subCategory);
        console.log(spatial);
        console.log(format1);
        console.log(this.uploadForm.fields);
        console.log(this.uploadForm.coordinateSystem);
        console.log(this.uploadForm.resourceDescription);
        console.log(this.uploadForm.size);
        console.log(this.uploadForm.state);
        console.log(this.uploadForm.isUploaded);
        console.log(this.resources.length + 1);*/
  const jsonData = {
    "indexName": 'resource_list',
    "docId": pid1,
    "jsonString": {
      "id": this.resources.length + 1,
      "type": this.uploadForm.fileType,
      "subCategory": this.uploadForm.subCategory,
      "name": name1,
      "is_spatial": spatial,
      "format": format1,
      "field": this.uploadForm.fields,
      "coordinate": this.uploadForm.coordinateSystem,
      "description": this.uploadForm.resourceDescription,
      "fileSize": this.uploadForm.size,
      "state": this.uploadForm.state,
      "isUploaded": this.uploadForm.isUploaded,
    }
  };

  try {
    // 发送 POST 请求
    const postResponse = await fetch('/api/textquery/insertDoc', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // 设置为 JSON 格式
      },
      body: JSON.stringify(jsonData)
    });

    if (postResponse.ok) {
      const postResponseData = await postResponse.text();
      console.log('Post Response:', postResponseData);

      // 检查响应是否成功
      if (postResponseData.includes('Index:') && postResponseData.includes('ID:') && postResponseData.includes('Version:')) {
        console.log('服务器上传成功');

       
        
        try {
          // 构造 URL，包含查询参数
          const url = `/api/systemtable/api/insertData?pid=${pid1}&name=${name1}&type=${this.uploadForm.fileType}&subCategory=${this.uploadForm.subCategory}&isspatial=${spatial}&format=${format1}&field=${this.uploadForm.fields}&coordinate=${this.uploadForm.coordinateSystem}&description=${this.uploadForm.resourceDescription}&fileSize=${this.uploadForm.size}&state=${this.uploadForm.state}&isUploaded=${this.uploadForm.isUploaded}&id=${this.resources.length + 1}`;

          const getResponse = await fetch(url, { method: 'GET' });
          console.log(getResponse);
          if (getResponse.ok) {
            const getResponseData = await getResponse.text();
            if (getResponseData === 'Data added successfully.') {
              console.log('数据库上传成功');
              alert('上传成功');
              this.uploadProgress = 100;
            } else {
              console.log('数据库上传失败:', getResponseData);
              alert('上传失败');
            }
          } else {
            console.error('GET 请求失败，状态码:', getResponse.status);
          }
        } catch (error) {
          console.error('GET 请求错误:', error);
        }
      } else {
        console.log('无法解析 POST 响应:', postResponseData);
        alert('上传失败');
      }
    } else {
      console.error('POST 请求失败，状态码:', postResponse.status);
    }
  } catch (error) {
    console.error('POST 请求错误:', error);
  }
    
},


async waitForUploadComplete() {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      if (this.uploadComplete) {
        clearInterval(interval);  // 停止轮询
        resolve();  // 返回并继续执行后续代码
      }
    }, 500);  // 每500毫秒检查一次
  });
},
// 使用 async/await 进行异步处理
async sendPostRequest() {
  
  const pid1=this.uploadForm.pid;
  this.uploadForm.isUploaded = true;
  let spatial = false;
  if (this.uploadForm.isSpatialData === "是") {
    spatial = true;
  };

  // 提取文件名和格式
  let name1 = "", format1 = "";

  if (this.selectedFiles && this.selectedFiles.length > 0) {
    // 查找是否有 .shp 文件
    const shpFile = this.selectedFiles.find(file => file.name.endsWith('.shp'));
    if (shpFile) {
      name1 = shpFile.name.split('.').slice(0, -1).join('.'); // 取 .shp 文件的名称
      format1 = 'shp'; // 格式设为 shp
    }
  } else {
    // 单文件的情况，直接根据文件类型来处理
    if (this.selectedFile.name.endsWith('.zip')) {
      await this.delay(2000);
      // 第一个请求: 上传文件
      console.log(pid1)
      name1 = this.selectedFile.name.split('.').slice(0, -1).join('.');
      const srResponse = await fetch(`/api/ingestion/upload?pid=${pid1}`, { 
        method: 'GET'
      });

      const responseData = await srResponse.text();

      // 如果查询失败，直接返回
      if (!responseData.includes('File path:')) {
        console.error('查询失败:', responseData);
        this.$message.error('查询失败，请重试');
        return; // 如果查询失败，停止执行
      }

      // 匹配并提取格式
      const formatMatch = responseData.match(/Format:\s*(\w+)/);
      if (formatMatch) {
        format1 = formatMatch[1].toLowerCase();
      } else {
        console.error('未找到文件格式');
        this.$message.error('未找到文件格式');
        return;
      }
    } else {
      // 单文件的情况，直接提取文件名和格式
      name1 = this.selectedFile.name.split('.').slice(0, -1).join('.');
      format1 = this.selectedFile.name.split('.').pop().toLowerCase();
    }
  }

  console.log('name1:', name1, 'format1:', format1);

  // 如果无法确定文件名和格式，提示用户
  if (!name1 || !format1) {
    console.error('无法确定文件的名称或格式');
    this.$message.error('无法确定文件的名称或格式');
    return;
  }
  console.log(pid1);
        console.log(name1);
        console.log(this.uploadForm.fileType);
        console.log(this.uploadForm.subCategory);
        console.log(spatial);
        console.log(format1);
        console.log(this.uploadForm.fields);
        console.log(this.uploadForm.coordinateSystem);
        console.log(this.uploadForm.resourceDescription);
        console.log(this.uploadForm.size);
        console.log(this.uploadForm.state);
        console.log(this.uploadForm.isUploaded);
        console.log(this.resources.length + 1);
  const jsonData = {
    "indexName": 'resource_list',
    "docId": pid1,
    "jsonString": {
      "id": this.resources.length + 1,
      "type": this.uploadForm.fileType,
      "subCategory": this.uploadForm.subCategory,
      "name": name1,
      "is_spatial": spatial,
      "format": format1,
      "field": this.uploadForm.fields,
      "coordinate": this.uploadForm.coordinateSystem,
      "description": this.uploadForm.resourceDescription,
      "fileSize": this.uploadForm.size,
      "state": this.uploadForm.state,
      "isUploaded": this.uploadForm.isUploaded,
    }
  };

  try {
    // 发送 POST 请求
    const postResponse = await fetch('/api/textquery/insertDoc', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // 设置为 JSON 格式
      },
      body: JSON.stringify(jsonData)
    });

    if (postResponse.ok) {
      const postResponseData = await postResponse.text();
      console.log('Post Response:', postResponseData);

      // 检查响应是否成功
      if (postResponseData.includes('Index:') && postResponseData.includes('ID:') && postResponseData.includes('Version:')) {
        console.log('服务器上传成功');

        console.log(pid1);
        console.log(name1);
        console.log(this.uploadForm.fileType);
        console.log(this.uploadForm.subCategory);
        console.log(spatial);
        console.log(format1);
        console.log(this.uploadForm.fields);
        console.log(this.uploadForm.coordinateSystem);
        console.log(this.uploadForm.resourceDescription);
        console.log(this.uploadForm.size);
        console.log(this.uploadForm.state);
        console.log(this.uploadForm.isUploaded);
        console.log(this.resources.length + 1);
        
        try {
          // 构造 URL，包含查询参数
          const url = `/api/systemtable/api/insertData?pid=${pid1}&name=${name1}&type=${this.uploadForm.fileType}&subCategory=${this.uploadForm.subCategory}&isspatial=${spatial}&format=${format1}&field=${this.uploadForm.fields}&coordinate=${this.uploadForm.coordinateSystem}&description=${this.uploadForm.resourceDescription}&fileSize=${this.uploadForm.size}&state=${this.uploadForm.state}&isUploaded=${this.uploadForm.isUploaded}&id=${this.resources.length + 1}`;

          const getResponse = await fetch(url, { method: 'GET' });
          console.log(getResponse);
          if (getResponse.ok) {
            const getResponseData = await getResponse.text();
            if (getResponseData === 'Data added successfully.') {
              console.log('数据库上传成功');
              alert('上传成功');
              this.uploadProgress = 100;
            } else {
              console.log('数据库上传失败:', getResponseData);
              alert('上传失败');
            }
          } else {
            console.error('GET 请求失败，状态码:', getResponse.status);
          }
        } catch (error) {
          console.error('GET 请求错误:', error);
        }
      } else {
        console.log('无法解析 POST 响应:', postResponseData);
        alert('上传失败');
      }
    } else {
      console.error('POST 请求失败，状态码:', postResponse.status);
    }
  } catch (error) {
    console.error('POST 请求错误:', error);
  }
},




  
  handleCloseProgressDialog() {
    this.uploadProgressVisible = false; // 关闭弹窗
  },
 

   
    showUploadModal() {
      this.uploadDialogVisible = true;
    },
    
    
    deleteResource(resource) {
      this.deleteTarget = resource;
      this.deleteConfirmDialogVisible = true;
    },
    confirmDelete() {
    const resource = this.deleteTarget;
    console.log(resource.pid);

    // 先调用/api/ingestion/upload?pid=接口进行删除（DELETE方法）
    fetch(`/api/ingestion/upload?pid=${resource.pid}`, {
        method: 'DELETE'
    })
  .then(response => response.text())
  .then(responseData => {
        if (responseData.includes('Folder and all files deleted successfully for pid')) {
            console.log('第一个接口删除成功，继续删除ES服务器数据');
            // 再删除另一个数据库中的数据 (使用 POST 请求)
            return fetch(`/api/textquery/deleteDoc?indexName=resource_list&docId=${resource.pid}`, {
                method: 'POST'
            });
        } else {
            console.error('第一个接口删除失败:', responseData);
            alert('删除失败');
            throw new Error('第一个接口删除失败');
        }
    })
  .then(response => response.text())
  .then(responseData => {
        if (responseData.includes('Document deleted with ID:')) {
            console.log('es服务器删除成功');

            // 继续删除主数据库中的数据
            return fetch(`/api/systemtable/api/deleteData?pid=${resource.pid}`, {
                method: 'GET'
            });
        } else {
            console.error('es服务器删除失败:', responseData);
            alert('删除失败');
            throw new Error('es服务器删除失败');
        }
    })
  .then(response => response.text())
  .then(responseData => {
        if (responseData === 'Data resource deleted successfully.') {
            console.log('数据库删除成功');
            alert('删除成功');
            // 从本地资源列表中删除该资源
            this.resources = this.resources.filter(item => item!== resource);
            this.resetDeleteConfirm();
        } else {
            console.error('数据库删除失败:', responseData);
            alert('删除失败');
        }
    })
  .catch(error => {
        console.error('请求错误:', error);
    });
    this.deleteConfirmDialogVisible = false;
    setTimeout(() => {
        this.refreshData();
    }, 1000);
},


    cancelDelete() {
      this.resetDeleteConfirm();
    },
    resetDeleteConfirm() {
      this.deleteConfirmDialogVisible = false;
      this.deleteTarget = null;
    },
    downloadResource(resource) {
      // 执行下载逻辑
    },


    async importToDatabase(resource) {
    let filePath = '';
    const state = "是";
    const state1 = true;
    console.log(resource.pid);
    const pid1 = resource.pid;

    try {
        // 第一个请求: 上传文件
        const srResponse = await fetch(`/api/ingestion/upload?pid=${pid1}`, {
            method: 'GET'
        });
        const responseData = await srResponse.text();

        // 使用响应内容检查查询是否成功
        if (!responseData.includes('File path:')) {
            console.error('查询失败:', responseData);
            alert("入库失败！");
            return; // 如果查询失败，停止执行
        }

        // 提取文件路径
        const pathMatch = responseData.match(/File path:\s*([^,]+)/);
        if (pathMatch) {
            filePath = pathMatch[1]; // 提取到的文件路径
            console.log('提取到的文件路径:', filePath);
        } else {
            console.log('未找到文件路径');
            return; // 如果未找到文件路径，停止执行
        }

        // 确定文件格式
        const fileExtension = resource.format;
        let url = '';
        let payloadKey = '';
        let method = 'POST'; // 默认使用 POST 方法

        switch (fileExtension) {
            case 'shp':
                // SHP 文件使用 GET 方法，将路径作为查询字符串参数
                url = `/api/shp/importShapefile?filePath=${filePath}`;
                method = 'GET';
                break;
            case 'png':
                url = '/api/raster_tiles/rasterTiles/upload';
                payloadKey = 'filePath';
                break;
            case '3dtiles':
                url = '/api/3d_tiles/uploadFromPath';
                payloadKey = 'tilesetPath';
                break;
            case 'geojson':
            case'mvt':
                url = '/api/vector_tiles/api/tiles/uploadDirectory';
                payloadKey = 'directoryPath';
                break;
            default:
                console.error(`未知文件类型，无法处理: ${fileExtension}`);
                return;
        }

        // 发送入库请求
        let rkResponse, rkData, importSuccess;

        if (method === 'GET') {
            // GET 请求形式
            rkResponse = await fetch(url, { method: 'GET' });
            rkData = await rkResponse.text();
            console.log(rkData);
            importSuccess = rkData.includes('导入成功');
        } else {
            // POST 请求使用 FormData 发送
            const formData = new FormData();
            formData.append(payloadKey, filePath);

            rkResponse = await fetch(url, {
                method: 'POST',
                body: formData
            });
            importSuccess = rkResponse.ok;
        }

        // 检查入库是否成功
        if (importSuccess) {
            console.log("文件批量导入成功:", rkData || rkResponse.status);

            // 第三个请求: 更新 ES 服务器数据
            const jsonData = {
                indexName: 'resource_list', // 设置 indexName
                docId: resource.pid, // 设置 docId
                jsonString: { state: "是" }
            };

            const serverResponse = await fetch('/api/textquery/updateDoc', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const serverData = await serverResponse.text();
            if (!serverResponse.ok ||!serverData.includes('Index: resource_list') ||!serverData.includes('ID:')) {
                console.error('服务器更新失败:', serverData);
                alert("入库失败！");
                return; // 服务器更新失败，停止执行
            }

            console.log('服务器更新成功');

            // 第四个请求: 更新数据库
            const dbResponse = await fetch(
                `/api/systemtable/api/updateData?pid=${resource.pid}&state=${state1}&type=${resource.type}&subCategory=${resource.subCategory}&description=${resource.description}&isUploaded=${resource.isUploaded}`,
                { method: 'GET' }
            );

            if (!dbResponse.ok) {
                console.error('数据库请求失败，状态码:', dbResponse.status);
                alert("入库失败！");
                return; // 数据库请求失败，停止执行
            }

            const dbData = await dbResponse.text();
            if (dbData.includes('updated successfully')) {
                console.log('资源已成功入库');
                this.$message.success('资源已成功入库');
            } else {
                console.error('数据库更新失败:', dbData);
                alert("入库失败！");
            }
        } else {
            console.error("文件批量导入失败:", rkData || rkResponse.status);
            alert("入库失败！");
        }

    } catch (error) {
        console.error('请求错误:', error);
        alert("入库失败！");
    }
},

    logout() {
      localStorage.removeItem('username'); // 删除 'username'
localStorage.removeItem('region');   // 删除 'region'
      this.$router.push('/system');
    }
  },
  
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

.el-upload__input {
  display: none;
}

.custom-input {
margin-top: 5px;
  margin-left: 40px;
  width: 60%;
  display: flex;
}

.dialog-footer-content {
  text-align: right;
}

.search-box {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.compact-button {
  margin-left: 5px;
  margin-bottom: 5px;
}
.actions {
  display: flex;
  flex-direction: column; /* 让每个 .button-group 在垂直方向排列 */
  gap: 10px; /* 设置 .button-group 之间的间距 */
}

.button-group {
  display: flex;
  gap: 10px; /* 设置按钮之间的间距 */
}

.action-button {
  flex: 1; /* 使按钮平分 .button-group 宽度 */
}
</style>