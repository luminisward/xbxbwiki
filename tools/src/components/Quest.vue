<template>
  <el-row :gutter="20">
    <el-col :span="6">
      <div class="form-group">
        <label>地点</label>
        <el-input v-model="quest.place"></el-input>
      </div>
      <div class="form-group">
        <label>条件</label>
        <el-input v-model="quest.requirement"></el-input>
      </div>
      <div class="form-group">
        <label>任务NPC</label>
        <el-input v-model="quest.npc"></el-input>
      </div>
      <div class="form-group">
        <label>报酬额</label>
        <el-input v-model="reward.gil"></el-input>
      </div>
      <div class="form-group">
        <label>EXP</label>
        <el-input v-model="reward.exp"></el-input>
      </div>
      <div class="form-group">
        <label>SP</label>
        <el-input v-model="reward.sp"></el-input>
      </div>
      <div class="form-group">
        <label>奖励道具</label>
        <el-input type="textarea" autosize v-model="reward.items"></el-input>
      </div>
      <div class="form-group">
        <label>游戏内任务说明文本</label>
        <el-input type="textarea" autosize v-model="quest.text"></el-input>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="form-group">
        <label>任务步骤</label>
        <el-input type="textarea" autosize v-model="quest.step"></el-input>
      </div>
    </el-col>
    <el-col :span="12">
        <el-card >
            <div slot="header">
                结果 <el-button type="text" id="button1">复制</el-button>
            </div>
            <div id="quest-results">
<pre>
======  ======

&lt;WRAP half&gt;
|地点  |  {{quest.place}}|
|条件  |  {{quest.requirement}}|
|NPC  |  {{quest.npc}}|
|报酬额  |  {{reward.gil}}|
|EXP  |  {{reward.exp}}|
|SP  |  {{reward.sp}}|
|奖励道具  |  {{items}}|
&lt;/WRAP&gt;

{{text}}

===== 任务步骤 =====

{{step}}
</pre>
            </div>     
        </el-card>
    </el-col>
  </el-row>
</template>

<script>
  function convertNewline(multilineText){
      if(multilineText){
          return multilineText.replace(/\n/g,'\\\\\n');
      }
  }
  function convertMultilineInOneline(multilineText){
      if(multilineText){
          return multilineText.replace(/\n/g,'\\\\ ');
      }
  }
  function convertOrderList(multilineText){
      if(multilineText){
          var ret = '';
          var multilineArray = multilineText.split('\n');
          for(var i in multilineArray){
              multilineArray[i] = '  - ' + multilineArray[i];
              ret += multilineArray[i] + '\n';
          }
          return ret;
      }
  }
  var copy_url = new Clipboard(
    '#button1', {
      text: function() {
        return document.getElementById('quest-results').innerText;
        }
      }
    );


  export default {
    data() {
      return{
        reward: {},
        quest: {},
      }
    },
    computed: {
      items: function(){
        return convertMultilineInOneline(this.reward.items);
      },
      text: function(){
        return convertNewline(this.quest.text);
      },
      step: function(){
        return convertOrderList(this.quest.step);
      },
      keypoint: function(){
        return convertOrderList(this.quest.keypoint);
      },
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
