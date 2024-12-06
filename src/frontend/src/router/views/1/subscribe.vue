<template>
  <Layout>
    <div>
      <el-card>
        <div class="content">
          <h1>个人订阅</h1>
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
            <el-table-column prop="subscription_id" label="订阅ID"></el-table-column>
            <el-table-column prop="user_id" label="用户ID"></el-table-column>
            <el-table-column prop="enterprise_id" label="企业ID"></el-table-column>
            <el-table-column prop="company_name" label="企业名称"></el-table-column>
            <el-table-column prop="condition" label="监控条件"></el-table-column>
            <el-table-column prop="created_at" label="创建时间">
              <template slot-scope="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="280" align="center">
              <template slot="header">
                <span style="display: flex; justify-content: center;">操作</span>
              </template>
              <template slot-scope="scope">
                <div class="button-group">
                  <el-button 
                    size="mini" 
                    type="primary"
                    @click="viewCreditReport(scope.row)">
                    信用报告
                  </el-button>
                  <el-button 
                    size="mini" 
                    type="success"
                    @click="viewDecisionReport(scope.row)">
                    决策报告
                  </el-button>
                  <el-button 
                    size="mini" 
                    type="danger" 
                    @click="handleUnsubscribe(scope.row)">
                    取消订阅
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
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      filteredResources: []
    };
  },

  mounted() {
    this.loadSubscriptionData();
  },

  methods: {
    // 加载订阅数据
    loadSubscriptionData() {
      // 初始化示例数据
      this.initializeExampleData();
      // 从localStorage获取数据并显示在表格中
      const data = JSON.parse(localStorage.getItem('subscriptionData') || '[]');
      this.filteredResources = data;
    },

    // 初始化示例数据
    initializeExampleData() {
      const exampleData = [
        {
          subscription_id: "SUB001",
          user_id: "USER001",
          enterprise_id: "ENT001",
          company_name: "阿里巴巴科技有限公司",
          condition: "信用评分 > 80",
          created_at: "2024-01-15T10:30:00Z"
        },
        {
          subscription_id: "SUB002",
          user_id: "USER001",
          enterprise_id: "ENT002",
          company_name: "腾讯科技有限公司",
          condition: "信用评分 > 85",
          created_at: "2024-01-14T14:20:00Z"
        },
        {
          subscription_id: "SUB003",
          user_id: "USER001",
          enterprise_id: "ENT003",
          company_name: "华为技术有限公司",
          condition: "信用评分 > 90",
          created_at: "2024-01-13T09:15:00Z"
        },
        {
          subscription_id: "SUB004",
          user_id: "USER001",
          enterprise_id: "ENT004",
          company_name: "中国建设银行",
          condition: "信用评分 > 95",
          created_at: "2024-01-12T16:45:00Z"
        },
        {
          subscription_id: "SUB005",
          user_id: "USER001",
          enterprise_id: "ENT005",
          company_name: "中国石化有限公司",
          condition: "信用评分 > 75",
          created_at: "2024-01-11T11:25:00Z"
        }
      ];

      // 检查是否已经初始化过
      if (!localStorage.getItem('subscriptionData')) {
        localStorage.setItem('subscriptionData', JSON.stringify(exampleData));
      }
    },

    // 保存订阅数据
    saveSubscriptionData() {
      try {
        localStorage.setItem('subscriptionData', JSON.stringify(this.filteredResources));
      } catch (error) {
        console.error('保存数据失败:', error);
        this.$message.error('保存数据失败');
      }
    },

    // 格式化日期
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString();
    },

    // 更新取消订阅方法
    async handleUnsubscribe(row) {
      try {
        await this.$confirm('确认取消该订阅?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          buttonsSortOrder: ['confirm', 'cancel']
        });

        // 调用取消订阅API
        const response = await fetch(`/subscriptions/${row.subscription_id}`, {
          method: 'DELETE',
          headers: {
            // 'Authorization': `Bearer ${localStorage.getItem('token')}` // 暂时注释token验证
          }
        });

        if (response.ok) {
          const result = await response.json();
          this.$message.success(result.message);
          
          // 从本地数据中移除该订阅
          this.filteredResources = this.filteredResources.filter(
            item => item.subscription_id !== row.subscription_id
          );
          
          // 保存更新后的数据到localStorage
          this.saveSubscriptionData();
        } else {
          throw new Error('取消订阅失败');
        }
      } catch (error) {
        if (error.message === '取消订阅失败') {
          this.$message.error('取消订阅失败');
        } else {
          this.$message.info('已取消操作');
        }
        console.error('取消订阅错误:', error);
      }
    },

    // 搜索方法
    handleSearch() {
      if (!this.searchQuery) {
        this.loadSubscriptionData();
        return;
      }

      const query = this.searchQuery.toLowerCase();
      const data = JSON.parse(localStorage.getItem('subscriptionData') || '[]');
      
      this.filteredResources = data.filter(item => 
        item.company_name.toLowerCase().includes(query) ||
        item.subscription_id.toLowerCase().includes(query) ||
        item.enterprise_id.toLowerCase().includes(query)
      );
    },

    // 刷新数据
    async refreshData() {
      this.loadSubscriptionData();
      this.$message.success('数据已刷新');
    },

    // 分页方法
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.currentPage = 1;
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
    },

    // 查看信用报告
    viewCreditReport(row) {
      this.$router.push({
        name: 'Credit-report',
        params: { enterpriseId: row.enterprise_id }
      });
    },

    // 查看决策报告
    viewDecisionReport(row) {
      this.$router.push({
        name: 'Decision-report',
        params: { enterpriseId: row.enterprise_id }
      });
    }
  }
};
</script>

<style scoped>
.content {
  margin-top: 10px;
  padding: 10px;
}

.search-box {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.button-group {
  display: flex;
  gap: 5px;
  justify-content: center;
}

.button-group .el-button--mini {
  padding: 5px 8px;
  margin: 0;
}

.el-table th {
  text-align: center;
}
</style>
