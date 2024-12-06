<template>
  <div>
    <el-row class="navbar" type="flex" justify="start" align="middle">
      <el-col :span="24" class="navbar-left">
        <img src="../assets/6.png" alt="Logo" class="logo-image" />
        <span class="logo-text">城市存量空间数据场景化<br>集成与一体化管理系统</span>
      </el-col>
    </el-row>

    <div class="bg">
      <div class="left-side">
        <div class="welcome-text">
          欢迎使用
        </div>
      </div>
      <div class="right-side">
        <div class="login-box" v-if="!showRegister">
          <h2>用户登录</h2>
          <form @submit.prevent="handleSubmit">
            <input type="text" placeholder="用户名" v-model="username" required>
            <input type="password" placeholder="密码" v-model="password" required>
            <div class="buttons">
              <input type="submit" value="登录">
              <button type="button" @click="showRegister = true">注册账号</button>
            </div>
          </form>
        </div>
        <div class="register-box" v-else>
          <h2>用户注册</h2>
          <form @submit.prevent="handleRegister">
            <input type="text" placeholder="用户名" v-model="newUsername" required>
            <input type="password" placeholder="密码" v-model="newPassword" required>
            <select v-model="region" required>
              <option disabled value="">选择所属地区</option>
              <option value="北京">北京</option>
              <option value="重庆">重庆</option>
              <option value="深圳">深圳</option>
              <option value="宁波">宁波</option>
            </select>
            <div class="buttons">
              <input type="submit" value="注册">
              <button type="button" @click="showRegister = false">返回登录</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      newUsername: '',
      newPassword: '',
      region: '',
      showRegister: false,
    };
  },
  methods: {
    handleSubmit() {
      const url = `/api/signup/login?username=${encodeURIComponent(this.username)}&password=${encodeURIComponent(this.password)}`;

      fetch(url, {
        method: 'GET',
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.text(); // 处理文本响应
      })
      .then(data => {
        const trimmedData = data.trim(); // 移除首尾空格
        
        if (trimmedData.includes("登录成功！")) {
          alert('登录成功！');
          const regionMatch = trimmedData.match(/您的地区是：(\S+)/);
      if (regionMatch) {
        localStorage.setItem('username', this.username);
localStorage.setItem('region', regionMatch[1].replace('。', ''));
console.log(regionMatch[1]);
      }
      

        
          this.$router.push('/system/admin'); // 跳转到 admin 页面
        } else {
          alert('用户名或密码错误');
        }
      })
      .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
        alert('登录请求失败');
      });
    },

    handleRegister() {
      if (this.newUsername && this.newPassword && this.region) {
        const url = `/api/signup/register?username=${encodeURIComponent(this.newUsername)}&password=${encodeURIComponent(this.newPassword)}&region=${encodeURIComponent(this.region)}`;

        fetch(url, {
          method: 'GET',
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
          return response.text(); // 处理文本响应
        })
        .then(data => {
          const trimmedData = data.trim(); // 移除首尾空格
          if (trimmedData === "注册成功！") {
            alert('注册成功！');
            this.showRegister = false; // 返回登录界面
            this.username = this.newUsername; // 预填用户名
            this.password = this.newPassword; // 预填密码
          } else {
            alert(trimmedData); // 显示其他响应内容
          }
        })
        .catch(error => {
          console.error('There was a problem with your fetch operation:', error);
          alert('注册请求失败');
        });
      } else {
        alert('请填写所有注册信息');
      }
    }
  }
};
</script>

<style scoped>
body, html {
  height: 100%;
  margin: 0;
  font-family: Arial, sans-serif;
}

.bg {
  background-image: url('../assets/image3.jpg'); 
  height: 100vh;
  width: 100vw;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.left-side, .right-side {
  width: 50%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-box, .register-box {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: center;
}

.login-box h2, .register-box h2 {
  margin-bottom: 20px;
}

.login-box input[type="text"], .login-box input[type="password"],
.register-box input[type="text"], .register-box input[type="password"],
.register-box select {
  width: calc(100% - 20px); 
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box; 
  appearance: none; 
}

.register-box select {
  -webkit-appearance: none; 
  -moz-appearance: none; 
  appearance: none; 
  background-color: white; 
  background-image: none; 
}

.buttons {
  display: flex;
  justify-content: space-between;
}

.login-box input[type="submit"], .register-box input[type="submit"],
.login-box button, .register-box button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background: #007BFF;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.login-box input[type="submit"]:hover, .register-box input[type="submit"]:hover,
.login-box button:hover, .register-box button:hover {
  background: #0056b3;
}

.welcome-text {
  font-size: 36px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.navbar {
  background-color: white; 
  width: 100%; 
  padding: 10px 0; 
  border-bottom: 1px solid #e7e7e7; 
  position: fixed; 
  top: 0; 
  left: 0; 
  z-index: 1000; 
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo-image {
  height: 60px; 
  margin-left: 20px; 
  margin-right: 20px; 
}

.logo-text {
  text-align: left; 
  font-size: 20px;
  font-weight: bold;
  color: #888; 
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2); 
}

.content {
  margin-top: 70px; 
}
</style>
