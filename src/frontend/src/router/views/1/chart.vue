<template>
  <Layout>
  <div>
    <el-row class="navbar" type="flex" justify="space-between" align="middle">
  <el-col :span="7" class="navbar-left">
    <span class="logo">城市存量空间数据场景化<br>集成与一体化管理系统</span>
  </el-col>
  <el-col :span="9" class="navbar-center">
    <el-menu mode="horizontal" default-active="1" class="el-menu-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
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

    <!-- Main Content -->
    <div class="main-content">
      <!-- 上部分，包含左边栏、中间栏和右边栏 -->
      
     

      <!-- 下部分，包含左边栏和右边栏 -->
      <div class="bottom-section">
        <div class="bottom-left-section">
          <!-- 模块D内容（DataLinks） -->
          <div class="table-container">
    <el-table
      :data="tableData"
      style="width: 100%"
      height="400">
      <el-table-column
        prop="ipAddress"
        label="数据链接"
        width="480">
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态">
      </el-table-column>
    </el-table>
  </div>
        </div>

        <div class="bottom-right-section">
          <!-- 模块E内容（DataLinkStatus） -->
          <div class="data-link-status">
            <el-table
      :data="tableData1"
      style="width: 100%">
      <el-table-column
        prop="ipAddress"
        label="IP 地址"
        width="150">
      </el-table-column>
      <el-table-column
        prop="computerName"
        label="计算机名"
        width="150">
      </el-table-column>
      <el-table-column
        prop="creationTime"
        label="创建时间"
        width="150">
      </el-table-column>
      <el-table-column
        prop="status"
        label="运行状态">
      </el-table-column>
    </el-table>

          </div>
        </div>
      </div>
    </div>
  </div>
</Layout>
</template>

<script>
import Layout from "../../layouts/main";


export default {
  name: 'YourComponentName',
  components: {
    Layout,

  },
 

  data () {
    return {

      username: localStorage.getItem('username'),// 读取存储的用户名
      region : localStorage.getItem('region'),
      tableData: [
        { ipAddress: 'mongodbc1192.168.***.221:12345/u_p/Box_1.glf', status: '正常' },
        { ipAddress: 'mongodbc/1192.168.***221:12345/u_p/B0x_3.gltf', status: '正常' },
        { ipAddress: 'mongodb://192.168.…,221:12345/up/ulian 4',status: '正常' },
        { ipAddress: 'mongodb://192.168.…,221:12345/u_pigis图形数据分析框架5.', status: '正常' },
        { ipAddress: 'mongodbc/192168.**221:12345/up/TEST-Yufang-Prvate-szteraln-也形24', status: '正常' },
        { ipAddress: 'mongodbc/1192.168**22112345u_p/SZAV12019 50GK2KmageServer1 7', status: '正常' },
        { ipAddress: 'mongodbc1192.168.221:12345/u_p/top_9',status: '正常' },
        { ipAddress: 'mongodbc/192168.**221:12345/up/TEST-Yufang-Prvate-szteraln-也形24', status: '正常' },
        { ipAddress: 'mongodbc/1192.168**22112345u_p/SZAV12019 50GK2KmageServer1 7', status: '正常' },
        { ipAddress: 'mongodbc1192.168.221:12345/u_p/top_9',status: '正常' }
      ],
      tableData1: [
        { ipAddress: '168.4.4.61:8090', computerName: 'suplic3dcloud-ion', creationTime: '-', status: '正常' },
        { ipAddress: '168.4.4.61:8090', computerName: 'suplic3dcloud-ion', creationTime: '-', status: '正常' },
        { ipAddress: '168.4.4.61:8090', computerName: 'suplic3dcloud-ion', creationTime: '-', status: '正常' },
        { ipAddress: '168.4.4.61:8090', computerName: 'suplic3dcloud-ion', creationTime: '-', status: '正常' },
        { ipAddress: '168.4.4.61:8090', computerName: 'suplic3dcloud-ion', creationTime: '-', status: '正常' },
        { ipAddress: '168.4.4.61:8090', computerName: 'suplic3dcloud-ion', creationTime: '-', status: '正常' },
  
      ]
    }
  },
  
  methods: {
    logout () {
      localStorage.removeItem('username'); // 删除 'username'
localStorage.removeItem('region');   // 删除 'region'

      this.$router.push('/system');
    },
    

  
  }
}
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
.el-main {
  padding: 10px;
}

.table-container, .data-link-status {

  margin-bottom: 0px;
  width: 700px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 设置阴影的偏移量、模糊半径和颜色 */
}

.top-traffic-stats {
  display: flex;
  flex-direction: column;
  height: 80px; /* 使模块高度填满 el-card */
  box-sizing: border-box; /* 包括边框和内边距在宽度和高度中 */
}

.top-traffic-stats .header {
  font-size: 16px; /* 减小标题字号 */
  margin: 0; /* 去除默认外边距 */
  padding-bottom: 10px; /* 添加底部内边距，防止紧贴内容 */
}

.top-traffic-stats .stats {
  font-size: 10px;
  flex: 1; /* 使内容区域占满剩余空间 */
  display: flex;
  align-items: center;
  justify-content: center; /* 内容居中对齐 */
  padding: 10px; /* 添加内边距，使内容与边缘保持一定距离 */
}


.center-section {
  margin-right: 0;
}
.right-section {
  display: flex;
  justify-content: center; /* 居中对齐右侧区域 */
}

.top-traffic-stats {
  padding: 20px;
  background-color: #fff; /* 模块背景色 */
  border: 1px solid #dcdcdc; /* 模块边界线 */
  border-radius: 5px; /* 边界圆角 */
  display: flex;
  flex-direction: column;
  height: 100%; /* 使模块充满容器 */
  width: 100%; /* 使模块充满容器宽度 */
  box-sizing: border-box; /* 包括边框和内边距在宽度和高度中 */
}

.header {
  align-self: flex-start; /* 标题靠左对齐 */
  margin: 0; /* 去除默认外边距 */
}

.stats {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center; /* 内容居中对齐 */
  width: 100%; /* 使内容区域充满模块宽度 */
  height:100%
}

.data {
  font-weight: bold;
}

.table-container , .data-link-status{
  max-height: 370px; /* 设置表格的最大高度 */
  
  width: 700px;
}

.el-card{
  
  border-radius: 4px; /* 设置圆角半径，调整边角的圆润程度 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 设置阴影的偏移量、模糊半径和颜色 */
  padding: 10px; /* 设置卡片内边距 */
}
.el-table {
  width: 100%;
  overflow: hidden; /* 避免额外的水平滚动条 */
  border: 1px solid #dcdcdc; /* 设置表格边框颜色，稍微深一点的灰色 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 设置阴影的偏移量、模糊半径和颜色 */
  padding: 16px; /* 设置卡片内边距 */
}

.el-table th, .el-table td {
  border-color: #1d1c1c; /* 表头和表格单元格的边框颜色 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 设置阴影的偏移量、模糊半径和颜色 */
  padding: 16px; /* 设置卡片内边距 */
}

.data {
  font-weight: bold;
}

.scrollable-table {
  max-height: 500px; /* Adjust the height as needed */
  overflow-y: auto;
}

.logout-button {
  padding: 5px 10px;
  background-color: #ff4d4f;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #ff7875;
}

/* Main Content Styles */
.main-content {
  background-color: #ecf0f1; 
  display: flex;
  flex-direction: column;
}

.top-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0px;
}

.left-section,.center-section,  .right-section, .bottom-left-section, .bottom-right-section {
  background-color: #ecf0f1; /* 边栏背景色 */
  padding: 10px;


}
.left-section{
padding-right: 5px;
}


.bottom-section {
  display: flex;
  justify-content: space-between;
}

.bottom-left-section, .bottom-right-section {
  flex: 1;  
  margin-right: 0px; /* 边栏右侧间距 */
}

.bottom-right-section {
  margin-right: 20px;
}
</style>
