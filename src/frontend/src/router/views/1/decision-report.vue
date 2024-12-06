<template>
  <Layout>
    <div class="decision-report">
      <el-card>
        <div class="enterprise-selector">
          <el-input
            v-model="inputEnterpriseId"
            placeholder="请输入企业ID"
            style="width: 300px; margin-right: 20px"
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
            <span class="report-title">企业决策报告</span>
            <el-button 
              type="primary" 
              size="small"
              @click="downloadReport">
              下载报告
            </el-button>
          </div>

          <el-tabs v-model="activeTab">
            <!-- 执行摘要 -->
            <el-tab-pane label="执行摘要" name="summary">
              <div class="info-section">
                <h3>执行摘要</h3>
                <div class="info-content">
                  <p>{{ report.executiveSummary || '暂无执行摘要信息' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 企业概况 -->
            <el-tab-pane label="企业概况" name="overview">
              <div class="info-section">
                <h3>企业历史沿革</h3>
                <div class="info-content">
                  <p>{{ report.companyHistory || '暂无企业历史信息' }}</p>
                </div>
              </div>
              <div class="info-section">
                <h3>行业分析</h3>
                <div class="info-content">
                  <p>{{ report.industryAnalysis || '暂无行业分析信息' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 财务分析 -->
            <el-tab-pane label="财务分析" name="finance">
              <div class="info-section">
                <h3>财务报表分析</h3>
                <div class="info-content">
                  <p>{{ report.financialAnalysis || '暂无财务分析信息' }}</p>
                </div>
              </div>
              <div class="info-section">
                <h3>现金流量分析</h3>
                <div class="info-content">
                  <p>{{ report.cashFlowAnalysis || '暂无现金流量分析' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 业务分析 -->
            <el-tab-pane label="业务分析" name="business">
              <div class="info-section">
                <h3>产品与服务</h3>
                <div class="info-content">
                  <p>{{ report.productAnalysis || '暂无产品分析信息' }}</p>
                </div>
              </div>
              <div class="info-section">
                <h3>研发能力</h3>
                <div class="info-content">
                  <p>{{ report.rdCapability || '暂无研发能力信息' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 竞争分析 -->
            <el-tab-pane label="竞争分析" name="competition">
              <div class="info-section">
                <h3>竞争优势</h3>
                <div class="info-content">
                  <p>{{ report.competitiveAdvantages || '暂无竞争优势信息' }}</p>
                </div>
              </div>
              <div class="info-section">
                <h3>竞争劣势</h3>
                <div class="info-content">
                  <p>{{ report.competitiveDisadvantages || '暂无竞争劣势信息' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 管理团队 -->
            <el-tab-pane label="管理团队" name="management">
              <div class="info-section">
                <h3>核心团队</h3>
                <div class="info-content">
                  <p>{{ report.managementTeam || '暂无管理团队信息' }}</p>
                </div>
              </div>
              <div class="info-section">
                <h3>公司治理</h3>
                <div class="info-content">
                  <p>{{ report.corporateGovernance || '暂无公司治理信息' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 风险评估 -->
            <el-tab-pane label="风险评估" name="risk">
              <div class="info-section">
                <h3>风险分析</h3>
                <div class="info-content">
                  <p>{{ report.riskAssessment || '暂无风险评估信息' }}</p>
                </div>
              </div>
            </el-tab-pane>

            <!-- 投资建议 -->
            <el-tab-pane label="投资建议" name="investment">
              <div class="info-section">
                <h3>盈利预测</h3>
                <div class="info-content">
                  <p>{{ report.profitForecast || '暂无盈利预测信息' }}</p>
                </div>
              </div>
              <div class="info-section">
                <h3>投资建议</h3>
                <div class="info-content">
                  <p>{{ report.investmentAdvice || '暂无投资建议' }}</p>
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
  name: 'DecisionReport',
  components: {
    Layout
  },
  data() {
    return {
      inputEnterpriseId: '',
      selectedEnterprise: '',
      enterprises: [],
      activeTab: 'summary',
      report: {
        // 示例数据
        executiveSummary: '该企业是行业领先的技术创新企业，具有强大的研发能力和市场竞争力近年来业绩稳定增长，财务状况健康...',
        companyHistory: '公司成立于2010年，经过十余年发展，已成为行业领军企业。主要里程碑包括...',
        industryAnalysis: '所处行业市场规模约2000亿元，年增长率保持在15%以上。公司市场份额约20%，排名行业第二...',
        financialAnalysis: '近三年营收复合增长率达25%，净利润率稳定在15%以上。资产负债率控制在50%以下...',
        cashFlowAnalysis: '经营活动现金流充沛，近三年年均现金流量比率保持在1.2以上，现金流状况良好...',
        productAnalysis: '主要产品线包括企业级软件解决方案、云服务平台等。产品市场占有率稳步提升...',
        rdCapability: '研发投入占营收10%以上，拥有核心专利200余项，在AI领域具有领先优势...',
        competitiveAdvantages: '技术领先、品牌影响力强、客户粘性高、销售网络完善...',
        competitiveDisadvantages: '国际市场份额较小、部分核心技术仍需突破...',
        managementTeam: '管理团队平均行业经验超过15年，多数具有知名企业工作背景...',
        corporateGovernance: '建立了完善的公司治理结构，内部控制体系健全...',
        riskAssessment: '主要风险包括技术迭代风险、市场竞争加剧风险、人才流失风险等...',
        profitForecast: '预计未来三年营收将保持20%以上增长，净利润增速15-20%...',
        investmentAdvice: '建议买入。基于公司强劲的业绩增长、领先的市场地位和良好的发展前景...'
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
        const response = await fetch(`/subscriptions/${enterpriseId}/decision-report`);
        if (response.ok) {
          const data = await response.json();
          this.report = data;
        } else {
          throw new Error('获取决策报告失败');
        }
      } catch (error) {
        console.error('获取决策报告失败:', error);
        this.$message.error('获取决策报告失败');
      } finally {
        this.loading = false;
      }
    },

    // 下载决策报告
    async downloadReport() {
      if (!this.selectedEnterprise) {
        this.$message.warning('请先选择企业');
        return;
      }

      try {
        // 使用正确的API接口路径
        const response = await fetch(`/subscriptions/${this.selectedEnterprise}/decision-report`, {
          headers: {
            // 'Authorization': `Bearer ${localStorage.getItem('token')}` // 暂时注释token验证
          }
        });

        if (response.ok) {
          // 获取文件名
          const contentDisposition = response.headers.get('content-disposition');
          let filename = `决策报告_${this.selectedEnterprise}.pdf`;
          if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
            if (filenameMatch && filenameMatch[1]) {
              filename = filenameMatch[1].replace(/['"]/g, '');
            }
          }

          // 下载文件
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = filename;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);

          this.$message.success('报告下载成功');
        } else if (response.status === 404) {
          const error = await response.json();
          throw new Error(error.message || '未找到决策报告');
        } else {
          throw new Error('下载失败');
        }
      } catch (error) {
        console.error('下载决策报告失败:', error);
        this.$message.error(error.message || '下载决策报告失败');
      }
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
    await this.loadEnterprises();
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
.decision-report {
  padding: 20px;
}

.enterprise-selector {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-input {
  width: 300px;
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
  text-align: justify;
}

.empty-tip {
  padding: 40px 0;
}
</style> 