<template>
  <el-tabs v-model="activeName" type="card" >
    <el-tab-pane label="任务" name="quest"><Quest/></el-tab-pane>
    <el-tab-pane label="敌人" name="blade">敌人</el-tab-pane>
    <el-tab-pane label="饰品" name="accessary"><Accessory/></el-tab-pane>
  </el-tabs>
</template>
<script>
  import Quest from './Quest.vue'
  import Accessory from './Accessory.vue'
  export default {
    components: {
      Quest,
      Accessory
    },
    data() {
      return {
        activeName: 'quest'
      }
    },
  }

</script>