<template>
  <Layout>

  <div>
   
    <el-card>
      <div class="content">
        <h1>企业信息总览</h1>
        <el-row class="search-box">
          <el-col :span="8">
            <el-input 
              v-model="searchQuery" 
              placeholder="搜索企业..."
              @input="handleSearch"
              clearable>
            </el-input>
          </el-col>
          <el-col :span="16" style="text-align: right;">

            <el-button @click="refreshData">刷新</el-button>
          </el-col>
        </el-row>

        <el-table :data="filteredResources" style="width: calc(100% - 40px); margin: 0 20px;" class="custom-table">
          <el-table-column prop="enterprise_id" label="企业ID"></el-table-column>
          <el-table-column prop="company_name" label="企业名称"></el-table-column>
          <el-table-column prop="industry" label="所属行业"></el-table-column>
          <el-table-column prop="bill_medium" label="票据介质"></el-table-column>
          <el-table-column prop="system_notes" label="系统备注"></el-table-column>
          <el-table-column prop="company_notes" label="企业备注"></el-table-column>
          <el-table-column prop="software_acquisition_notes" label="数据获取说明"></el-table-column>
          <el-table-column label="操作" width="220" align="right">
            <template slot="header">
              <span style="display: flex; justify-content: center;">操作</span>
            </template>
            <template slot-scope="scope">
              <div class="button-group">
                <el-button 
                  size="mini" 
                  type="primary" 
                  @click="handleSubscribe(scope.row)">
                  订阅
                </el-button>
                <el-button 
                  size="mini" 
                  type="warning" 
                  @click="handleEdit(scope.row)">
                  修改
                </el-button>
                <el-button 
                  size="mini" 
                  type="danger" 
                  @click="handleDelete(scope.row)">
                  删除
                </el-button>
                <el-button 
                  size="mini" 
                  type="info" 
                  @click="handleDisclosure(scope.row)">
                  披露信息
                </el-button>
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

        <el-dialog
          title="添加企业"
          :visible.sync="dialogVisible"
          width="50%"
          @close="resetForm"
        >
          <el-form :model="form" label-width="120px">
            <el-form-item label="企业ID">
              <el-input v-model="form.enterprise_id"></el-input>
            </el-form-item>
            <el-form-item label="企业名称">
              <el-input v-model="form.company_name"></el-input>
            </el-form-item>
            <el-form-item label="所属行业">
              <el-input v-model="form.industry"></el-input>
            </el-form-item>
            <el-form-item label="票据介质">
              <el-select v-model="form.bill_medium" placeholder="请选择票据介质">
                <el-option label="电子" value="电子"></el-option>
                <el-option label="纸质" value="纸质"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="系统备注">
              <el-input type="textarea" v-model="form.system_notes"></el-input>
            </el-form-item>
            <el-form-item label="企业备注">
              <el-input type="textarea" v-model="form.company_notes"></el-input>
            </el-form-item>
            <el-form-item label="数据获取说明">
              <el-input type="textarea" v-model="form.software_acquisition_notes"></el-input>
            </el-form-item>
          </el-form>
          <div class="dialog-footer-content">
            <el-button type="primary" @click="confirmUpload">确 定</el-button>
            <el-button @click="resetForm">取 消</el-button>
          </div>
        </el-dialog>

        <!-- 文件选择输入 -->
        <input
          type="file"
          ref="fileInput"
          accept=""
          style="display: none;"
          @change="handleFileChange"
        />
      </div>
    </el-card>
  </div>
</Layout>
</template>

<script>

import Layout from "../../layouts/main";



export default {
  components: {
    Layout,

  },
  data() {
    return {
      username: localStorage.getItem('username'),// 读取存储的用户名

      enterprises: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      form: {
        enterprise_id: '',
        company_name: '',
        industry: '',
        bill_medium: '',
        system_notes: '',
        company_notes: '',
        software_acquisition_notes: ''
      },
      selectedFileName: '',
      selectedFile: null,
      filteredResources: []
    };
  },

  mounted() {
    // const token = localStorage.getItem('token');
    // if (!token) {
    //   this.$router.push('/login');
    //   return;
    // }
    this.loadEnterpriseData();
  },

  methods: {
    // 获取企业列表
    async fetchEnterprises() {
      try {
        const response = await fetch('/enterprises');
        if (response.ok) {
          const data = await response.json();
          this.resources = data;
        } else {
          throw new Error('Failed to fetch enterprises');
        }
      } catch (error) {
        console.error('获取企业列表失败:', error);
        this.$message.error('获取企业列表失败');
      }
    },

    // 添加企业
    async addEnterprise() {
      try {
        const response = await fetch('/enterprises', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });

        if (response.ok) {
          this.$message.success('添加企业成功');
          this.dialogVisible = false;
          await this.fetchEnterprises();
        } else {
          throw new Error('Failed to add enterprise');
        }
      } catch (error) {
        console.error('添加企业失败:', error);
        this.$message.error('添加企业失败');
      }
    },

    // 保留原始的loadEnterpriseData方法（已注释）
    /*async loadEnterpriseData() {
      // const token = localStorage.getItem('token');
      // if (!token) {
      //   this.$router.push('/login');
      //   return;
      // }

      try {
        const response = await fetch('/enterprises', {
          // headers: {
          //   'Authorization': `Bearer ${token}`
          // }
        });
        
        if (response.ok) {
          const data = await response.json();
          this.filteredResources = data;
        } else {
          throw new Error('Failed to load enterprises');
        }
      } catch (error) {
        console.error('加载数据失败:', error);
        this.$message.error('加载数据失败');
      }
    }, */

    // 新的临时版本的loadEnterpriseData方法
    loadEnterpriseData() {
      // 初始化示例数据
      this.initializeExampleData();
      // 从localStorage获取数据并显示在表格中
      const data = JSON.parse(localStorage.getItem('enterpriseData') || '[]');
      this.filteredResources = data;
    },

    // initializeExampleData方法保持不变
    initializeExampleData() {
      const exampleData = [
        {
          enterprise_id: "E001",
          company_name: "阿里巴巴科技有限公司",
          industry: "互联网",
          bill_medium: "电子",
          system_notes: "系统对接完成",
          company_notes: "主营电子商务",
          software_acquisition_notes: "使用API对接"
        },
        {
          enterprise_id: "E002",
          company_name: "腾讯科技有限公司",
          industry: "互联网",
          bill_medium: "电子",
          system_notes: "需要更新接口",
          company_notes: "主营社交和游戏",
          software_acquisition_notes: "使用SDK对接"
        },
        {
          enterprise_id: "E003",
          company_name: "中国石化有限公司",
          industry: "能源",
          bill_medium: "纸质",
          system_notes: "传统对接方式",
          company_notes: "石油化工企业",
          software_acquisition_notes: "人工录入"
        },
        {
          enterprise_id: "E004",
          company_name: "华为技术有限公司",
          industry: "通信技术",
          bill_medium: "电子",
          system_notes: "系统运行正常",
          company_notes: "通信设备制造商",
          software_acquisition_notes: "专有协议对接"
        },
        {
          enterprise_id: "E005",
          company_name: "中国建设银行",
          industry: "金融",
          bill_medium: "电子",
          system_notes: "银行系统对接",
          company_notes: "国有商业银行",
          software_acquisition_notes: "银行专线对接"
        }
      ];

      // 检查是否已经初始化过
      if (!localStorage.getItem('enterpriseData')) {
        localStorage.setItem('enterpriseData', JSON.stringify(exampleData));
      }
    },

    // 保存企业数据
    saveEnterpriseData() {
      try {
        localStorage.setItem('enterpriseData', JSON.stringify(this.filteredResources));
      } catch (error) {
        console.error('保存数据失败:', error);
        this.$message.error('保存数据失败');
      }
    },

    // 修改原有的删除方法
    handleDelete(row) {
      // const token = localStorage.getItem('token');
      // if (!token) {
      //   this.$router.push('/login');
      //   return;
      // }

      this.$confirm('确认删除该企业?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        buttonsSortOrder: ['confirm', 'cancel']
      }).then(async () => {
        try {
          const response = await fetch(`/api/enterprise/delete/${row.enterprise_id}`, {
            method: 'DELETE',
            // headers: {
            //   'Authorization': `Bearer ${token}`
            // }
          });
          
          if (response.ok) {
            this.$message.success('删除成功');
            this.refreshData();
          } else {
            this.$message.error('删除失败');
          }
        } catch (error) {
          console.error('删除请求错误:', error);
          this.$message.error('删除失败');
        }
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },

    // 修改原有的添加/编辑方法
    async sendPostRequest() {
      // const token = localStorage.getItem('token');
      // if (!token) {
      //   this.$router.push('/login');
      //   return;
      // }

      const formData = { ...this.form };
      
      try {
        // 检查是否是编辑模式
        const existingIndex = this.filteredResources.findIndex(
          item => item.enterprise_id === formData.enterprise_id
        );

        if (existingIndex >= 0) {
          // 更新现有数据
          this.filteredResources[existingIndex] = formData;
        } else {
          // 添加新数据
          this.filteredResources.push(formData);
        }

        // 保存到localStorage
        this.saveEnterpriseData();
        
        this.$message.success(existingIndex >= 0 ? '更新成功' : '添加成功');
        this.resetForm();
      } catch (error) {
        console.error('操作失败:', error);
        this.$message.error('操作失败');
      }
    },

    // 搜索方法
    handleSearch() {
      if (!this.searchQuery) {
        this.loadEnterpriseData();
        return;
      }

      const query = this.searchQuery.toLowerCase();
      const data = JSON.parse(localStorage.getItem('enterpriseData') || '[]');
      
      this.filteredResources = data.filter(item => 
        item.enterprise_id.toLowerCase().includes(query) ||
        item.company_name.toLowerCase().includes(query) ||
        item.industry.toLowerCase().includes(query)
      );
    },

    // 处理页码变化
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.paginateResources(); // 改为 paginateResources
    },
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.currentPage = 1;
      this.paginateResources(); // 为 paginateResources
    },


    // 刷新数据
    async refreshData() {
      await this.loadEnterpriseData();
      this.$message.success('数据已刷新');
    },
    
    paginateResources() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredResources.slice(start, end);
    },

    async searchResource() {
      const fields = ['name', 'path'];
      const uniqueResults = new Set();
      const jsonRegex = /<div>\s*({.*?})\s*<\/div>/g; // 正则表达式匹配 div 中的 JSON 字符串

      try {
        for (const field of fields) {
          const url = `/api/textquery/fuzzySearch?indexName=map_list&fieldName=${field}&searchTerm=${this.searchQuery}&fuzziness=1`;

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
    console.log(this.filteredResources)
    this.paginateResources(); // 更新分页后的数据
  } catch (error) {
    console.error('Error fetching search results:', error);
  }
},

    async confirmDelete(tileset) {
      try {
        await this.$confirm('确认删除该任务?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          buttonsSortOrder: ['confirm', 'cancel']
        });

    const tileset1 = tileset;  // 获取传入的 tileset

    // 先删除另一个数据库中数据 (使用 POST 请求)
    const esResponse = await fetch(`/api/textquery/deleteDoc?indexName=map_list&docId=${tileset1.pid}`, {
      method: 'POST',
    });
    
    const esResponseData = await esResponse.text();
    if (esResponseData.includes(`Document deleted with ID:`)) {
      console.log('es服务器删除成功');


      // 继续删除主数据库中的数据
      const dbResponse = await fetch(`/api/systemtable/api/deleteslice?pid=${tileset1.pid}`, {
        method: 'GET'
      });

      const dbResponseData = await dbResponse.text();
      if (dbResponseData.includes('Slice') && dbResponseData.includes('deleted successfully.')) {
        console.log('数据库删除成功');
        alert('删除成功');
        
        // 从本地资源列表中删除该资源
        this.tilesets = this.tilesets.filter(item => item !== tileset1);
        this.updateLocalStorage();  // 更新本地存储
        this.resetDeleteConfirm();  // 重置删除确认的状态
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
  }

  // 关闭删除确认对话框
  this.deleteConfirmVisible = false;

  // 延迟调用 refreshData 函数
  setTimeout(() => {
    this.refreshData();
  }, 1000);
},



    showUploadModal() {
      this.dialogVisible = true;
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFileName = file.name;
        this.form.inputPath = file.name; // 更新form.inputPath以便后续操作
        this.selectedFile = file;
      }
    },
    chooseFile() {
      this.$refs.fileInput.click();
    },
    resetForm() {
      this.dialogVisible = false;
      this.form = {
        enterprise_id: '',
        company_name: '',
        industry: '',
        bill_medium: '',
        system_notes: '',
        company_notes: '',
        software_acquisition_notes: ''
      };
      this.selectedFileName = '';
      this.selectedFile = null;
    },
    validateLevel() {
      const level = this.form.level;
      const reg = /^(0|[1-9]|1[0-8])$/;
      if (!reg.test(level)) {
        this.form.level = level.slice(0, -1); // 若不符条件，删除最后输入的字符
      }
    },
    
    confirmUpload() {
      if (this.validateForm()) {  // 添加表单验证
        this.sendPostRequest();
      }
    },
    /*async sendPostRequest() {
      const formData = {
        enterprise_id: this.form.enterprise_id,
        company_id: this.form.company_id,
        company_name: this.form.company_name,
        industry: this.form.industry,
        bill_medium: this.form.bill_medium,
        system_notes: this.form.system_notes,
        company_notes: this.form.company_notes,
        software_acquisition_notes: this.form.software_acquisition_notes
      };

      try {
        const response = await fetch('/api/enterprise/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        });

        if (response.ok) {
          this.$message.success('添加成功');
          this.refreshData();
          this.resetForm();
        } else {
          this.$message.error('添加失败');
        }
      } catch (error) {
        console.error('请求错误:', error);
        this.$message.error('请求失败');
      }
    },

  /*  confirmSelection() {
  const now = new Date().toLocaleString();
  const newResource = {
    name: this.form.dataName,
    path: this.form.inputPath,
    time: now,
    rank: this.form.level,  
    number: Math.pow(2, this.form.level * 2),
    current: 0,
    state: '待处理',
    progress: '0%'
  };

  this.resetForm();
},*/

    updateLocalStorage() {
      localStorage.setItem('tilesets', JSON.stringify(this.tilesets));
    },
    
    
    

    // 处理订阅
    async handleSubscribe(row) {
      try {
        const response = await fetch(`/enterprises/${row.enterprise_id}/subscribe`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const result = await response.json();
          this.$message.success(result.message);
        } else {
          const error = await response.json();
          throw new Error(error.message);
        }
      } catch (error) {
        console.error('订阅失败:', error);
        this.$message.error(error.message || '订阅失败');
      }
    },

    // 处理修改
    handleEdit(row) {
      this.form = { ...row };  // 复制当前行数据到表单
      this.dialogVisible = true;  // 打开编辑对话框
    },

    // 处理删除
    /*handleDelete(row) {
      this.$confirm('确认删除该企业?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const response = await fetch(`/api/enterprise/delete/${row.enterprise_id}`, {
            method: 'DELETE'
          });
          
          if (response.ok) {
            this.$message.success('删除成功');
            this.refreshData();
          } else {
            this.$message.error('删除失败');
          }
        } catch (error) {
          console.error('删除请求错误:', error);
          this.$message.error('删除失败');
        }
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },*/

    // 处理披露信息
    async handleDisclosure(row) {
      try {
        const response = await fetch(`/enterprises/${row.enterprise_id}/disclosures`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (response.ok) {
          const disclosures = await response.json();
          
          // 格式化披露信息用于显示
          const formattedDisclosures = disclosures.map(item => {
            const date = new Date(item.disclosure_date).toLocaleString();
            return `日期: ${date}\n信息: ${item.disclosure_info}`;
          }).join('\n\n');

          this.$alert(formattedDisclosures, '企业披露信息', {
            confirmButtonText: '确定',
            dangerouslyUseHTMLString: true
          });
        } else {
          throw new Error('获取披露信息失败');
        }
      } catch (error) {
        console.error('获取披露信息错误:', error);
        this.$message.error('获取披露信息失败');
      }
    },

    // 添加表单验证方法
    validateForm() {
      if (!this.form.enterprise_id || !this.form.company_name) {
        this.$message.warning('企业ID和企业名称为必填项');
        return false;
      }
      return true;
    }
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
  text-decoration: none; /* 标悬停时移除下划线 */
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
.search-box {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.search-box input {
  padding: 8px;
  margin-right: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-box button {
  padding: 8px 16px;
  background-color: #27a5d7;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-box button:hover {
  background-color: #34c5de;
}

.el-form-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.el-form-item label {
  width: 100px; /* 统一标签的宽度 */
  text-align: right; /* 标签右对齐 */
  padding-right: 5px; /* 标签和输框之间的间距 */
}

.el-form-item .el-input,
.el-form-item .el-select,
.el-form-item .el-button {
  flex: 1; /* 输入框和选择框拉伸以充剩余空间 */
}

.el-form-item .el-row {
  display: flex;
  align-items: center;
}

.el-form-item .el-input {
  width: 100%; /* 输入框占满剩余宽度 */
  padding-right: 15px;
}

.el-form-item .el-button {
  margin-left: 8px; /* 选择文件按钮和输入框之间的间距 */
}

.dialog-footer-content {
  display: flex;
  justify-content: flex-end;
  gap: 10px; /* 按钮之间的间距 */
  margin-top: 20px;
}

.el-table {
  width: 100%;
  margin: 0 20px;
}

.el-table .actions {
  display: flex;
  justify-content: space-between;
}

.el-dialog {
  height: 60%; /* 调整弹窗高度 */
  max-height: 80vh; /* 限制最大高度 */
}


.dialog-footer-content {
  display: flex;
  justify-content: flex-end;
}

.el-form-item {
  margin-bottom: 20px;
}

.upload-demo {
  display: inline-block;
}

.selected-file {
  margin-left: 10px;  
  color: #409EFF;
}

.compact-button {
  height: 30px;
  padding: 4px 8px !important;
  margin: 4px 2px !important;
}

.clear-button{
  margin-top: 20px;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.compact-button {
  margin: 0 5px;
  padding: 5px 10px;
}

.el-button--mini {
  font-size: 12px;
}

.button-group {
  display: flex;
  gap: 5px; /* 设置按钮之间的间距 */
  justify-content: flex-end; /* 改为右对齐 */
}

.button-group .el-button--mini {
  padding: 5px 8px;
  margin: 0;
}

/* 添加表头样式 */
.el-table th.is-right {
  text-align: right;
  padding-right: 8px; /* 可以根据需要调整这个值 */
}

/* 更新表头样式 */
.el-table th {
  text-align: center;
}

</style>
