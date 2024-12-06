<template>
  <Layout>
    <div class="credit-report">
      <el-card>
        <div class="enterprise-selector">
          <el-input
            v-model="inputEnterpriseId"
            placeholder="请输入企业ID"
            style="width: 300px"
            @keyup.enter.native="handleEnterpriseIdInput"
          >
            <el-button 
              slot="append" 
              icon="el-icon-search"
              @click="handleEnterpriseIdInput">
              查询
            </el-button>
          </el-input>

          <el-select
            v-model="selectedEnterprise"
            filterable
            remote
            placeholder="请输入企业名称搜索"
            style="width: 300px"
            :remote-method="searchEnterprises"
            :loading="loading"
            @change="handleEnterpriseChange"
          >
            <el-option
              v-for="item in enterprises"
              :key="item.enterprise_id"
              :label="item.company_name"
              :value="item.enterprise_id">
              <span style="float: left">{{ item.company_name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                {{ item.enterprise_id }}
              </span>
            </el-option>
          </el-select>
        </div>

        <div v-if="selectedEnterprise" class="report-content">
          <div class="header-actions">
            <span class="report-title">企业信用报告</span>
            <el-button 
              type="primary" 
              size="small"
              @click="downloadReport">
              下载报告
            </el-button>
          </div>

          <el-tabs v-model="activeTab">
            <!-- 企业基本信息 -->
            <el-tab-pane label="企业基本信息" name="basic">
              <div class="info-section">
                <h3>企业概况</h3>
                <div class="info-content">
                  <p>{{ report.companyOverview || '暂无企业概况信息' }}</p>
                </div>
              </div>

              <div class="info-section">
                <h3>注册信息</h3>
                <div class="info-content">
                  <p>{{ report.registrationInfo || '暂无注册信息' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 信用评价信息 -->
            <el-tab-pane label="信用评价" name="credit">
              <div class="info-section">
                <div class="credit-info">
                  <div class="credit-score">
                    <h3>信用评分</h3>
                    <el-progress type="circle" :percentage="report.creditScore"></el-progress>
                  </div>
                  <div class="credit-level">
                    <h3>信用等级</h3>
                    <div class="level-text">{{ report.creditLevel }}</div>
                  </div>
                </div>
              </div>
            </el-tab-pane>

            <!-- 财务信息 -->
            <el-tab-pane label="财务信息" name="finance">
              <div class="info-section">
                <h3>财务报表摘要</h3>
                <div class="info-content">
                  <p>{{ report.financialSummary || '暂无财务报表摘要' }}</p>
                </div>
              </div>

              <div class="info-section">
                <h3>财务比率分析</h3>
                <div class="info-content">
                  <p>{{ report.financialRatioAnalysis || '暂无财务比率分析' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 银行信贷信息 -->
            <el-tab-pane label="银行信贷" name="bank">
              <div class="info-section">
                <h3>信贷记录</h3>
                <div class="info-content">
                  <p>{{ report.loanRecordDescription || '暂无信贷记录' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 公共记录信息 -->
            <el-tab-pane label="公共记录" name="public">
              <div class="info-section">
                <h3>法院诉讼记录</h3>
                <div class="info-content">
                  <p>{{ report.lawsuitDescription || '暂无法院诉讼记录' }}</p>
                </div>
              </div>

              <div class="info-section">
                <h3>税务记录</h3>
                <div class="info-content">
                  <p>{{ report.taxDescription || '暂无税务记录' }}</p>
                </div>
              </div>

              <div class="info-section">
                <h3>行政处罚记录</h3>
                <div class="info-content">
                  <p>{{ report.penaltyDescription || '暂无行政处罚记录' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 经营信息 -->
            <el-tab-pane label="经营信息" name="operation">
              <div class="info-section">
                <h3>经营活动描述</h3>
                <div class="info-content">
                  <p>{{ report.businessDescription || '暂无经营活动描述' }}</p>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <div v-else class="empty-tip">
          <el-empty description="请选择要查看的企业"></el-empty>
        </div>
      </el-card>
    </div>
  </Layout>
</template>

<script>
import Layout from "../../layouts/main";

export default {
  name: 'CreditReport',
  components: {
    Layout
  },
  data() {
    return {
      inputEnterpriseId: '',
      selectedEnterprise: '',
      enterprises: [],
      activeTab: 'basic',
      activeNames: ['1'],
      report: {
        // 示例数据
        creditScore: 85,
        creditLevel: 'AAA',
        companyOverview: '该企业成立于2010年，是一家专注于技术创新的高科技企业。公司总部位于北京市朝阳区，现有员工500余人。主要从事软件开发和技术服务业务。',
        registrationInfo: '公司于2010年1月注册成立，注册资本1000万元人民币，统一社会信用代码91110000123456789X。经营范围包括计算机软件开发、技术咨询、技术服务等。',
        financialSummary: '截至2023年底，公司总资产达5亿元，较上年增长15%；营业收入3亿元，同比增长20%；净利润5000万元，同比增长25%。经营活动现金流量净额为8000万元。',
        financialRatioAnalysis: '公司资产负债率为45%，处于行业平均水平；流动比率2.5，速动比率2.0，均高于行业平均水平；净资产收益率达15%，显示较好的盈利能力。',
        loanRecordDescription: '企业现有银行贷款3笔，总额度1.5亿元，其中包括工商银行5000万元（正常），建设银行6000万元（正常），农业银行4000万元（正常）。所有贷款均按期还款，信用记录良好。',
        lawsuitDescription: '该企业近三年内有2起民事诉讼案件，均已结案。',
        taxDescription: '企业纳税信用等级为A级，无欠税记录。',
        penaltyDescription: '近五年内无重大行政处罚记录。',
        businessDescription: '公司主营业务为企业级软件开发和技术服务，在人工智能和大数据领域具有较强的技术优势。目前与多家世界500强企业建立了长期合作关系，市场份额稳步提升。'
      },
      loading: false
    };
  },
  methods: {
    // 加载企业列表
    async loadEnterprises() {
      try {
        this.loading = true;
        const response = await fetch('/api/enterprises'); // 假设的API端点
        if (response.ok) {
          const data = await response.json();
          this.enterprises = data;
        } else {
          throw new Error('Failed to load enterprises');
        }
      } catch (error) {
        console.error('加载企业列表失败:', error);
        this.$message.error('加载企业列表失败');
      } finally {
        this.loading = false;
      }
    },

    async searchEnterprises(query) {
      if (query !== '') {
        try {
          this.loading = true;
          const response = await fetch(`/enterprises/search?keyword=${encodeURIComponent(query)}`);
          if (response.ok) {
            const data = await response.json();
            this.enterprises = data;
          } else {
            throw new Error('搜索企业失败');
          }
        } catch (error) {
          console.error('搜索企业失败:', error);
          this.$message.error('搜索企业失败');
        } finally {
          this.loading = false;
        }
      }
    },

    // 处理企业选择变化
    async handleEnterpriseChange(enterpriseId) {
      if (!enterpriseId) {
        this.report = {};
        return;
      }
      
      try {
        this.loading = true;
        const response = await fetch(`/subscriptions/${enterpriseId}/credit-report`);
        if (response.ok) {
          const data = await response.json();
          this.report = data;
        } else {
          throw new Error('获取信用报告失败');
        }
      } catch (error) {
        console.error('获取信用报告失败:', error);
        this.$message.error('获取信用报告失败');
      } finally {
        this.loading = false;
      }
    },

    async downloadReport() {
      if (!this.selectedEnterprise) {
        this.$message.warning('请先选择企业');
        return;
      }

      try {
        const response = await fetch(`/subscriptions/${this.selectedEnterprise}/credit-report`, {
          headers: {
            // 'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `信用报告_${this.report.companyName}.pdf`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
        } else {
          throw new Error('下载失败');
        }
      } catch (error) {
        console.error('下载报告失败:', error);
        this.$message.error('下载报告失败');
      }
    },

    getStatusType(status) {
      const types = {
        '正常': 'success',
        '逾期': 'danger',
        '结清': 'info'
      };
      return types[status] || 'info';
    },

    // 新增：处理企业ID输入
    async handleEnterpriseIdInput() {
      if (!this.inputEnterpriseId) {
        this.$message.warning('请输入企业ID');
        return;
      }

      try {
        this.loading = true;
        this.selectedEnterprise = this.inputEnterpriseId;
        await this.handleEnterpriseChange(this.inputEnterpriseId);
      } catch (error) {
        console.error('加载企业信息失败:', error);
        this.$message.error('加载企业信息失败');
      } finally {
        this.loading = false;
      }
    }
  },
  async mounted() {
    const enterpriseId = this.$route.params.enterpriseId;
    if (enterpriseId) {
      this.inputEnterpriseId = enterpriseId;
      this.selectedEnterprise = enterpriseId;
      await this.handleEnterpriseChange(enterpriseId);
    }
  }
};
</script>

<style scoped>
.credit-report {
  padding: 20px;
}

.enterprise-selector {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.report-title {
  font-size: 18px;
  font-weight: bold;
}

.info-section {
  margin-bottom: 30px;
}

.info-section h3 {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
  color: #303133;
}

.info-content {
  padding: 0 20px;
}

.info-content p {
  margin: 12px 0;
  line-height: 1.6;
}

.label {
  display: inline-block;
  width: 120px;
  color: #606266;
  font-weight: 500;
}

.credit-info {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 20px;
}

.credit-score, .credit-level {
  text-align: center;
}

.level-text {
  font-size: 48px;
  font-weight: bold;
  margin-top: 20px;
  color: #409EFF;
}

.loan-records {
  padding: 0 20px;
}

.loan-item {
  padding: 15px 0;
}

.empty-tip {
  padding: 40px 0;
}

.el-divider {
  margin: 20px 0;
}
</style> 