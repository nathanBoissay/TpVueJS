<script>

export default {
    props: {
        todo : Object
    },
    methods:{
        remove : function(){
            this.$emit('remove',{id: this.todo.id})
        }
    },
    emits : ['remove']
}


</script>

<template>
    <div class="checkbox" v-bind:class="{'alert alert-success' : todo.ckecked } ">

    <label>
        <input type="checkbox" v:model="todo.ckecked"> {{ todo.text }}
        <input type="button" 
            class = "btn btn-danger"
            value="Supprimer"
            @click="remove">
    </label>

    </div>


</template>