<template>
  <el-row :gutter="20">
    <el-col :span="12">
      <div class="form-group">
          <label>名称</label>
          <el-input v-model="accessory.name"></el-input>
      </div>
      <div class="form-group">
          <label>出售价格</label>
          <el-input v-model="accessory.sellprice"></el-input> 
      </div>
      <div class="form-group">
          <label>说明</label>
          <el-input v-model="accessoryDescription"></el-input>
      </div>
      <el-col :span="8">
          <div class="form-group">
              <label>Lv1效果值</label>
              <el-input v-model="accessoryLv1effect"></el-input>
          </div>
          <div class="form-group">
              <label>Lv1获得地点</label>
              <el-input v-model="accessoryLocation1"></el-input>
          </div>
      </el-col>
      <el-col :span="8">
          <div class="form-group">
              <label>Lv2效果值</label>
              <el-input v-model="accessoryLv2effect"></el-input>
          </div>
          <div class="form-group">
              <label>Lv2获得地点</label>
              <el-input v-model="accessoryLocation2"></el-input>
          </div>
      </el-col>
      <el-col :span="8">
          <div class="form-group">
              <label>Lv3效果值</label>
              <el-input v-model="accessoryLv3effect"></el-input>
          </div>
          <div class="form-group">
              <label>Lv3获得地点</label>
              <el-input v-model="accessoryLocation3"></el-input>
          </div>
      </el-col>
    </el-col>
    <el-col :span="12">
      <el-card>
          <div slot="header">
              单页 <el-button type="text" id="button1">复制</el-button>
          </div>
          <div class="panel-body" id="accessory-results">
<pre>
====== {{accessory.name}} ======

^ 稀有度 ^ 说明 ^ 获得地点 ^
| 1 | {{makeDescription(accessoryDescription,accessoryLv1effect)}} | {{accessoryLocation1}} |
| 2 | {{makeDescription(accessoryDescription,accessoryLv2effect)}} | {{accessoryLocation2}} |
| 3 | {{makeDescription(accessoryDescription,accessoryLv3effect)}} | {{accessoryLocation3}} |

出售价格：{{accessory.sellprice}} G

===== 获取方式 =====

</pre>
          </div>     
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
  var copy_url = new Clipboard(
    '#button3', {
      text: function() {
        return document.getElementById('accessory-results').innerText;
      }
    }
  );

  export default {
    data() {
      return{
        accessory: {},
        accessoryDescription: '',
        accessoryLv1effect: '',
        accessoryLv2effect: '',
        accessoryLv3effect: '',
        accessoryLocation1: '',
        accessoryLocation2: '',
        accessoryLocation3: '',
      }
    },
    computed: {
      listElement: function(){
          if(this.accessoryLv1effect || this.accessoryLv2effect || this.accessoryLv3effect){
              this.accessoryLv1effect = this.accessoryLv1effect ? this.accessoryLv1effect : ' ';
              this.accessoryLv2effect = this.accessoryLv2effect ? this.accessoryLv2effect : ' ';
              this.accessoryLv3effect = this.accessoryLv3effect ? this.accessoryLv3effect : ' ';
              return this.accessoryDescription.replace('*','('+this.accessoryLv1effect+'/'+this.accessoryLv2effect+'/'+this.accessoryLv3effect+')');
          }else{
              return this.accessoryDescription;
          }
      },
    },
    methods: {
      makeDescription: function(description, effect){
        if(description){
          return description.replace('*',effect);
        }else{
          return '';
        }
      }
    }
  }
</script>

<style scoped>
  .form-group {
    margin-bottom: 10px;
  }
  label {
    display: inline-block;
    max-width: 100%;
    margin-bottom: 5px;
    font-weight: 700;
  }
</style>
