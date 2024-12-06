<template>
  <div>
    <el-row class="navbar" type="flex" justify="space-between" align="middle">
      <el-col :span="7" class="navbar-left">
        <span class="logo">城市存量空间数据场景化<br>集成与一体化管理系统</span>
      </el-col>
      <el-col :span="9" class="navbar-center">
        <el-menu mode="horizontal" default-active="4" class="el-menu-demo" background-color="#545c64" text-color="#fff"
          active-text-color="#ffd04b">
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
        <h1>场景列表</h1>

        <el-row class="search-box">
          <el-col :span="8">
            <el-button type="primary" @click="showUploadModal">新增场景</el-button>
          </el-col>
          <el-col :span="8">
            <el-input v-model="searchQuery" placeholder="搜索资源..."></el-input>
          </el-col>
          <el-col :span="8">
            <el-button type="primary" @click="searchResource">搜索</el-button>
            <el-button @click="refreshData">刷新</el-button>
          </el-col>
        </el-row>

        <el-table :data="filteredResources" class="custom-table" style="width: calc(100% - 40px); margin: 0 20px;">
          <el-table-column prop="sceneName" label="场景名称"></el-table-column>
          <el-table-column prop="sceneType" label="场景类型"></el-table-column>
          <el-table-column prop="user" label="作者"></el-table-column>
          <el-table-column prop="sceneDescription" label="场景描述"></el-table-column>
          <el-table-column prop="createtime" label="创建时间"></el-table-column>
          <el-table-column prop="edittime" label="编辑时间"></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <div class="actions">
                <el-button size="mini" type="danger" class="compact-button"
                  @click="deleteResource(scope.row)">删除</el-button>
                <el-button size="mini" class="compact-button" @click="editResource(scope.row)">编辑</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
          :page-sizes="[5, 10, 12, 15]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
          :total="scenes.length">
        </el-pagination>
      </div>
    </el-card>


    <!-- 上传弹窗 -->

    <!-- 场景集成弹窗 -->
    <el-dialog title="新增场景" :visible.sync="uploadDialogVisible" width="30%" @close="resetUploadForm">
      <el-form :model="uploadForm" label-width="120px">
        <el-form-item label="场景名称">
          <el-input v-model="uploadForm.sceneName"></el-input>
        </el-form-item>
        <el-form-item label="场景类型">
          <el-input v-model="uploadForm.sceneType"></el-input>
        </el-form-item>
        <el-form-item label="场景描述">
          <el-input type="textarea" v-model="uploadForm.sceneDescription"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="openElementSelectionDialog">场景集成</el-button>
        </el-form-item>
        <div class="dialog-footer-content">
          <el-button type="primary" @click="confirmUpload">确定</el-button>
          <el-button @click="resetUploadForm">取消</el-button>

        </div>
      </el-form>

      <!-- 场景要素选择弹窗 -->
      <el-dialog title="场景集成" :visible.sync="elementSelectionDialogVisible" width="70%" @close="resetElementSelection">
        <el-form label-width="400px">
          <el-form-item label="场景单元范围">
            <el-input v-model="spatialFileName" readonly placeholder="请选择文件"
              style="width: 200px; margin-right: 10px;margin-left: -250px;" />
            <el-button type="primary" size="mini" @click="chooseSpatialFile">
              {{ spatialFileName ? '导入' : '导入' }}
            </el-button>
          </el-form-item>

          <el-row class="dialog-content">
            <!-- 要素选取模块 -->
            <el-col :span="4" class="element-selection">
              <div class="section-header">
                <h3>要素选取</h3>
              </div>
              <el-tree v-if="isFileImported" :data="elementOptions" show-checkbox node-key="id" default-expand-all
                @check-change="handleElementCheckChange"></el-tree>
              <div v-else class="import-info">
                请先导入空间文件以加载动静态要素。
              </div>
            </el-col>

            <!-- 场景预览模块 -->
            <el-col :span="16" class="scene-display">
              <div class="section-header">
                <h3>场景预览</h3>
              </div>
              <div class="scene-content">
                <img v-for="item in selectedElements" :key="item.id" :src="item.image" class="overlay-image"
                  alt="叠加场景图片" />
              </div>
            </el-col>

            <!-- 已选择的要素模块 -->
            <el-col :span="4" class="selected-elements">
              <div class="section-header">
                <h3 style="text-align: right;">已选择的要素</h3>
              </div>
              <div class="element-cards">
                <el-card v-for="item in selectedElements" :key="item.id" class="element-card">
                  <div>{{ item.label }}</div>
                </el-card>
              </div>
            </el-col>
          </el-row>

          <div class="dialog-footer-content">
            <el-button type="primary" @click="confirmElementSelection">场景集成</el-button>
            <el-button @click="resetElementSelection">取消</el-button>
          </div>
        </el-form>
      </el-dialog>






    </el-dialog>
    <!-- 编辑场景弹窗 -->
    <el-dialog title="编辑场景" :visible.sync="editDialogVisible" width="30%" @close="resetEditForm">
      <el-form :model="editForm" label-width="120px">
        <el-form-item label="场景名称">
          <el-input v-model="editForm.sceneName"></el-input>
        </el-form-item>
        <el-form-item label="场景类型">
          <el-input v-model="editForm.sceneType"></el-input>
        </el-form-item>
        <el-form-item label="场景描述">
          <el-input type="textarea" v-model="editForm.sceneDescription"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="confirmEdit">确定</el-button>
          <el-button @click="resetEditForm">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!-- 删除确认弹窗 -->
    <el-dialog title="确认删除" :visible.sync="deleteConfirmVisible" width="30%" @close="resetDeleteConfirm">
      <p>确定要删除此场景吗？</p>
      <div class="dialog-footer-content">
        <el-button type="danger" @click="confirmDelete">确定</el-button>
        <el-button @click="resetDeleteConfirm">取消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

import { spatialOptions } from './spatialOptions.js';
import { generatePID } from './pidGenerator';
export default {

  data() {
    return {
      deleteConfirmVisible: false,
      sceneToDelete: null,
      editDialogVisible: false,
      editForm: {
        pid: '',
        sceneName: '',
        sceneType: '',
        sceneDescription: ''
      },
      scenes: [],
      username: localStorage.getItem('username'),// 读取存储的用户名
      region: localStorage.getItem('region'),// 读取存储的用户名
      paginatedScenes: [],
      filteredResources: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 5,
      uploadDialogVisible: false,
      elementSelectionDialogVisible: false,
      spatialFileName: '',
      isFileImported: false,
      deleteTarget: null,
      uploadForm: {
        pid: '',
        user: '',
        createtime: '',
        edittime: '',
        sceneName: '',
        sceneType: '',
        sceneDescription: '',
        spatialRange: [],
        spatialFile: null,
        selectedElements: [],
      },
      selectedFile: null, // 用于存储选中的文件
      spatialOptions, // 需要从服务器或本地加载的数据
      elementOptions: [
        {
          label: '动态要素',
          children: [
            { label: '温度传感器', id: 1, image: require('../assets/温度.png') },
            { label: '湿度传感器', id: 2, image: require('../assets/湿度.png') },
            { label: '烟雾传感器', id: 3, image: require('../assets/烟雾.png') },
            { label: '车', id: 4, image: require('../assets/车.png') },
            { label: '人', id: 9, image: require('../assets/人.png') },
          ],
        },
        {
          label: '静态要素',
          children: [
            { label: '地块', id: 5, image: require('../assets/9.png') },
            { label: '道路', id: 6, image: require('../assets/道路.png') },
            { label: '医院', id: 7, image: require('../assets/医院.png') },
            { label: '地铁站点', id: 8, image: require('../assets/地铁.png') },
          ],
        },
      ],
      selectedElements: [],
    };
  },

  computed: {
    filteredElementOptions() {
      if (!this.isFileImported) {
        // 如果文件未导入，则返回不包含子类的选项
        return this.elementOptions.map(option => ({
          ...option,
          children: [] // 去除子类
        }));
      }
      return this.elementOptions; // 否则返回完整数据
    },


  },

  methods: {
    async fetchscenes() {
      try {
        const response = await fetch('/api/systemtable/api/selectAllScenes');  // 替换为你的接口地址
        if (!response.ok) {
          throw new Error('Failed to fetch scenes');
        }

        const jsonData = await response.json();  // 以 JSON 格式获取数据
        console.log('Fetched scenes data:', jsonData);  // 打印原始响应

        // 处理数据
        if (Array.isArray(jsonData)) {
          // 遍历每个项目，并检查 edittime
          jsonData.forEach(item => {
            if (item.edittime === "null") {
              item.edittime = item.createtime;  // 将 createtime 的值赋给 edittime
            }
          });

          // 处理完后将数据赋值给 scenes
          this.scenes = jsonData;
          this.paginateScenes();  // 初始化分页
        } else {
          console.error('Expected an array, but got:', typeof jsonData);
        }
      } catch (error) {
        console.error('Error fetching scenes:', error);
      }
    },





    // 分页处理函数
    paginateScenes() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      this.filteredResources = this.scenes.slice(start, end);
    },

    // 处理页码变化
    handleCurrentChange(page) {
      this.currentPage = page;
      this.paginateScenes();
    },

    // 处理页面大小变化
    handleSizeChange(size) {
      this.pageSize = size;
      this.paginateScenes();
    },

    // 刷新数据
    refreshData() {
      this.fetchscenes();
    },


    async searchResource() {
      const fields = ['sceneName', 'sceneType', 'sceneDescription'];
      const uniqueResults = new Set();
      const jsonRegex = /<div>\s*({.*?})\s*<\/div>/g; // 正则表达式匹配 div 中的 JSON 字符串

      try {
        for (const field of fields) {
          const url = `/api/textquery/fuzzySearch?indexName=scenario_list&fieldName=${field}&searchTerm=${this.searchQuery}&fuzziness=1`;

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
        this.scenes = Array.from(uniqueResults).map(item => JSON.parse(item));
        console.log(this.scenes)
        this.paginateResources(); // 更新分页后的数据
      } catch (error) {
        console.error('Error fetching search results:', error);
      }
    },


    editResource(scene) {
      // 打开编辑弹窗，并初始化表单数据
      this.editForm = {
        pid: scene.pid,
        sceneName: scene.sceneName,
        sceneType: scene.sceneType,
        sceneDescription: scene.sceneDescription
      };
      this.editDialogVisible = true;
    },

    async confirmEdit() {
      const pid1 = this.editForm.pid;
      const sceneName1 = this.editForm.sceneName;
      const sceneType1 = this.editForm.sceneType;
      const sceneDescription1 = this.editForm.sceneDescription;
      const edittime1 = this.getCurrentTime()


      try {
        // 发送 POST 请求到服务器更新数据
        const jsonData = {
          indexName: 'scenario_list', // 设置 indexName
          docId: this.editForm.pid,    // 设置 docId
          jsonString: {
            sceneName: this.editForm.sceneName,
            sceneType: this.editForm.sceneType,
            sceneDescription: this.editForm.sceneDescription
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
        if (serverData.includes('Index: scenario_list') && serverData.includes('ID:')) {
          console.log('服务器更新成功');

          // 如果服务器返回更新成功，则继续更新数据库
          const dbResponse = await fetch(
            `/api/systemtable/api/updateScene?pid=${pid1}&sceneName=${sceneName1}&sceneType=${sceneType1}&sceneDescription=${sceneDescription1}&edittime=${edittime1}`,
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

    async sendPostRequest() {
      const user1 = this.username;
      const createtime1 = this.getCurrentTime();
      const createtime2 = new Date(createtime1.replace(' ', 'T'));
      const sceneName1 = this.uploadForm.sceneName;
      const sceneType1 = this.uploadForm.sceneType;
      const sceneDescription1 = this.uploadForm.sceneDescription;
      const selectedElements1 = this.uploadForm.selectedElements;
      const spatialRange1 = this.uploadForm.spatialRange;

      // 生成 PID
      const Pid = generatePID();
      this.uploadForm.pid = Pid;
      const pid1 = this.uploadForm.pid;

      // 构建要发送的表单数据
      const jsonData = {
        "indexName": 'scenario_list',
        "docId": this.uploadForm.pid,
        "jsonString": {
          "user": user1,
          "createtime": createtime2,
          "edittime": createtime2,
          "sceneName": sceneName1,
          "sceneType": sceneType1,
          "sceneDescription": sceneDescription1
        }
      };

      try {
        // 发送 POST 请求
        const postResponse = await fetch('/api/textquery/insertDoc', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json' // 设置为 JSON 格式
          },
          body: JSON.stringify(jsonData) // 发送原始 JSON 数据
        });

        if (postResponse.ok) {
          const postResponseData = await postResponse.text(); // 假设服务器返回纯文本响应
          console.log('Response:', postResponseData);

          if (postResponseData.includes('Index:') && postResponseData.includes('ID:') && postResponseData.includes('Version:')) {
            console.log('服务器上传成功');
            try {
              // 构建查询参数
              const url = `/api/systemtable/api/insertScene?pid=${pid1}&sceneName=${sceneName1}&sceneType=${sceneType1}&user=${user1}&sceneDescription=${sceneDescription1}&createtime=${createtime2}&edittime=${createtime2}`;

              // 发送 GET 请求
              const getResponse = await fetch(url, {
                method: 'GET'
              });

              if (getResponse.ok) {
                const getResponseData = await getResponse.text(); // 假设服务器返回纯文本响应
                console.log('Response:', getResponseData);

                if (getResponseData === 'Scene added successfully.') {
                  console.log('数据库上传成功');
                  alert('上传成功');
                  // 处理成功情况，例如显示提示或更新界面
                } else {
                  console.log('数据库上传失败:', getResponseData);
                  alert('上传失败');
                }
              } else {
                console.error('请求失败，状态码:', getResponse.status);
              }
            } catch (error) {
              console.error('请求错误:', error);
            }
          } else {
            console.log('无法解析响应:', postResponseData);
            return; // 终止执行，因为响应未正确处理
          }
        } else {
          console.error('服务器请求失败，状态码:', postResponse.status);
          alert('上传失败');
          return; // 终止执行，因为请求失败
        }
      } catch (error) {
        console.error('请求错误:', error);
        return; // 终止执行，因为请求错误
      }



      // 刷新数据
      this.refreshData();
    },


    async confirmDelete() {
      const scene = this.sceneToDelete;

      try {
        console.log(scene.pid);

        // 先删除另一个数据库中的数据 (使用 POST 请求)
        const esResponse = await fetch(`/api/textquery/deleteDoc?indexName=scenario_list&docId=${scene.pid}`, {
          method: 'POST',
        });

        const esResponseData = await esResponse.text();
        if (esResponseData.includes(`Document deleted with ID:`)) {
          console.log('es服务器删除成功');


          // 继续删除主数据库中的数据
          const dbResponse = await fetch(`/api/systemtable/api/deleteScene?pid=${scene.pid}`, {
            method: 'GET'
          });

          const dbResponseData = await dbResponse.text();
          if (dbResponseData === 'Scene deleted successfully.') {
            console.log('数据库删除成功');
            alert('删除成功');

            // 从本地资源列表中删除该资源
            this.resources = this.resources.filter(item => item !== scene);
            this.resetDeleteConfirm();
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



    cancelDelete() {
      this.resetDeleteConfirm();
    },

    getCurrentTime() {
      const now = new Date();
      const year = now.getFullYear();
      const month = (now.getMonth() + 1).toString().padStart(2, '0'); // 月份从0开始，所以要加1
      const day = now.getDate().toString().padStart(2, '0');
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      const seconds = now.getSeconds().toString().padStart(2, '0');

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`; // 返回自定义格式的字符串
    }

    ,
    // 更新时间的方法
    updateCurrentTime() {
      this.currentTime = this.getCurrentTime();
    },
    openElementSelectionDialog() {
      this.elementSelectionDialogVisible = true;
    },
    resetUploadForm() {
      this.uploadForm = {
        pid: '',
        user: '',
        createtime: '',
        edittime: '',
        sceneName: '',
        sceneType: '',
        sceneDescription: '',
        spatialRange: [],
        spatialFile: null,
        selectedElements: [],
      };
      this.uploadDialogVisible = false;
      this.spatialFileName = ''; // 清空文件名

    },


    chooseSpatialFile() {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = ''; // 允许选择所有格式的文件

      input.onchange = (event) => {
        const file = event.target.files[0];
        if (file) {
          this.uploadForm.spatialFile = file;
          this.spatialFileName = file.name; // 将文件名赋值给 spatialFileName
          this.isFileImported = true; // 文件选择后设置为 true

          // 如果有需要，可以在这里添加读取文件并更新 elementOptions 的逻辑
        }
      };
      input.click();
    },

    openElementSelectionDialog() {
      this.elementSelectionDialogVisible = true;
      this.isFileImported = false; // 打开弹窗时禁用选择
    },
    resetElementSelection() {
      this.uploadForm.spatialRange = [];
      this.uploadForm.spatialFile = null;
      this.uploadForm.selectedElements = [];
      this.selectedElements = []; // 这里也需要重置selectedElements
      this.spatialFileName = '';
      this.$nextTick(() => {
        const tree = this.$refs.elementTree; // 确保el-tree有ref属性
        if (tree) {
          tree.setCheckedKeys([]); // 清空所有勾选的项
        }
      });
      this.isFileImported = false; // 重置状态
      this.elementSelectionDialogVisible = false;
    },
    confirmElementSelection() {
      this.elementSelectionDialogVisible = false;
    },
    handleElementCheckChange(data, checked, indeterminate) {
      if (data.children) {
        // 忽略父节点
        return;
      }
      if (checked) {
        this.selectedElements.push(data);
      } else {
        this.selectedElements = this.selectedElements.filter(item => item.id !== data.id);
      }
    },
    confirmUpload() {
      if (this.uploadForm.sceneName && this.uploadForm.sceneType && this.uploadForm.sceneDescription && this.uploadForm.spatialRange && this.uploadForm.selectedElements) {

        // 处理文件上传逻辑
        this.sendPostRequest();
        this.resetUploadForm();
        this.resetElementSelection();

      } else {
        this.$message.error('请将信息填写完整');
      }
    },
    uploadResource() {
      const newScene = {
        user: this.username,
        createtime: this.getCurrentTime(),
        sceneName: this.uploadForm.sceneName,
        sceneType: this.uploadForm.sceneType,
        sceneDescription: this.uploadForm.sceneDescription,
        selectedElements: this.uploadForm.selectedElements,
        spatialRange: this.uploadForm.spatialRange,
      };

      this.scenes.push(newScene);
      localStorage.setItem('scenes', JSON.stringify(this.scenes));
    },

    confirmElementSelection() {
      this.elementSelectionDialogVisible = false;
    },
    logout() {
      localStorage.removeItem('username');
      localStorage.removeItem('region');
      this.$router.push('/system');
    },
    showUploadModal() {
      this.uploadDialogVisible = true;
    },
    handleFileChange(file) {
      this.selectedFile = file.raw; // 存储选中的文件
    },
    handleClose(done) {
      this.resetUploadForm();
      done();
    },



    // 重置编辑表单
    resetEditForm() {
      this.editForm = {
        pid: '',
        sceneName: '',
        sceneType: '',
        sceneDescription: '',
        spatialRange: [],
        selectedElements: [],
      };
      this.editDialogVisible = false;
    },
    // 删除场景
    deleteResource(scene) {
      this.sceneToDelete = scene;
      this.deleteConfirmVisible = true;
    },




    // 重置删除确认弹窗
    resetDeleteConfirm() {
      this.sceneToDelete = null;
      this.deleteConfirmVisible = false;
    },


    downloadResource(resource) {
      console.log('下载资源:', resource);
    },

  },
  mounted() {
    // 每秒钟更新一次时间
    this.timer = setInterval(this.updateCurrentTime, 1000);
    this.fetchscenes();
  },
  beforeDestroy() {
    // 在组件销毁前清除定时器
    clearInterval(this.timer);
  },

};
</script>

<style scoped>
.element-selection {
  border-right: 1px solid #ebeef5;
  padding-right: 10px;

}

.selected-elements {
  border-left: 1px solid #ebeef5;
  padding-left: 10px;
}




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
  text-decoration: none;
  /* 确保没有下划线 */
  color: inherit;
  /* 确保文字颜色继承自父元素 */
}

.navbar-center .el-menu-demo .el-menu-item a:hover {
  text-decoration: none;
  /* 鼠标悬停时移除下划线 */
}

.router-link-active {
  color: #ffd04b;
  /* 激活时文字颜色 */
  border-bottom: #ffd04b;
}

.navbar-left .logo {
  font-size: 16px;
  font-weight: bold;
  color: #1d1818;
  /* 灰色文字 */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  /* 文字虚化效果 */
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

.el-table {
  width: 90%;
  margin: 0 10px;
}

.el-table .actions {
  display: flex;


}


.el-dialog {
  height: 60%;
  /* 调整弹窗高度 */
  max-height: 80vh;
  /* 限制最大高度 */
}


.dialog-footer-content {
  margin-top: 30px;
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

.custom-table .el-table__body tr {
  height: 60px;
  /* 设置行高，例如 60px */
}

.custom-table .el-table__cell {
  padding: 20px 10px;
  /* 设置单元格的内边距来增加行高 */
}

.compact-button {
  height: 30px;

  margin: 5px 10px !important
}

/* 对话框内容区域 */
.dialog-content {
  display: flex;
  flex-wrap: nowrap;
  /* 防止子元素换行 */
}

/* 元素选择区域 */
.element-selection {
  padding: 10px;
  overflow: auto;
  /* 防止内容溢出 */
  margin-right: 20px
}

.scene-display {
  margin-right: 20px
}

.dialog-content {
  display: flex;
  align-items: stretch;
  /* 使所有列高度一致 */
}

.element-selection,
.scene-display,
.selected-elements {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 0px;
  overflow: hidden;
  overflow: auto;

}

.element-selection,
.selected-elements {
  display: flex;
  flex-direction: column;
}

.section-header {
  text-align: center;
  margin-bottom: 5px;
  padding: auto;
}

.scene-display {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.scene-content {
  border: 1px solid #ebeef5;
  padding: 20px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
}

.overlay-image {
  max-width: 100%;
  max-height: 100%;
}

.selected-elements {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: flex-start;
}

.element-card {
  padding: 0;
  width: 100px;
  margin-bottom: 2px;
  box-sizing: border-box;
  height: 30px;
  display: flex;
  align-items: center;
  /* 垂直居中 */
  justify-content: center;
  /* 水平居中 */
  overflow: hidden;
  /* 隐藏溢出文字 */
  text-overflow: ellipsis;
  /* 超出部分显示省略号 */
  white-space: nowrap;
  /* 禁止换行 */
}


.scene-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.scene-header {
  width: 100%;
  text-align: center;
  margin-bottom: 10px;
}

.scene-content {
  border: 1px solid #ebeef5;
  padding: 20px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
}

.overlay-image {
  max-width: 100%;
  max-height: 100%;
}


/* 场景展示区域 */
.scene-display {
  padding: 10px;
  position: relative;
  height: 400px;
  /* 设置合适的高度 */
  overflow: hidden;
}

/* 选中的元素区域 */
.selected-elements {
  padding-left: 20px;
  overflow-y: auto;
  /* 使内容溢出时可以滚动 */
}

/* 场景内容区域 */
.scene-content {
  position: relative;
  width: 100%;
  height: 100%;
}

/* 初始场景图片样式 */
.initial-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* 确保图片按比例适应容器 */
  z-index: 1;
}

/* 叠加图片样式 */
.overlay-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  /* 确保图片按比例适应容器 */
  z-index: 2;
}

.compact-form .el-form-item {
  margin-bottom: 0;
  /* 减少表单项之间的间距 */
}

.compact-form .compact-button {
  margin-left: 10px;
  /* 按钮和标签之间的间距 */
  padding: 0 10px;
  /* 调整按钮的内边距 */
}
</style>