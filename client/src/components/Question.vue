<template>
    <div class="card">
        <div class="card-header">
            <input v-if="editing" type="text" v-model="editText" @blur="doneEdit" @keyup.enter="doneEdit">
            <span v-else @dblclick="edit">{{ editText }}</span>
            <!-- <button class="btn btn-primary" @click="edit">Editer</button> -->
        </div>
        <div class="card-body">
            <ul>
                <li v-for="choice in choices" :key="choice">{{ choice }}</li>
            </ul>
        </div>
        <button class="btn btn-danger" @click="remove">Supprimer</button>
    </div>
</template>

<script>
export default {
    props: {
        question: Object
    },
    data() {
        return {
            reponses: [],
            editing: false,
            editText: this.question.title
        };
    },
    computed: {
        choices() {
            if (this.question.type === 'question_simple') {
                return [this.question.first_choix, this.question.second_choix]
            } else {
                return [this.question.first_choix, this.question.second_choix, this.question.third_choix, this.question.fourth_choix]
            }
        }
    },
    methods: {
        remove() {
            this.$emit('remove', this.question.id);
        },
        edit() {
            this.editing = true;
        },
        doneEdit() {
            this.editing = false;
            this.$emit('edit', this.question.id, this.editText);
            this.editQuestion(this.question.id, this.editText)
        },
        editQuestion(id, title) {
            fetch(`http://127.0.0.1:5000/questions/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title })
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Question modifiée')
                    } else {
                        console.error('Erreur lors de la modification de la question')
                    }
                })
                .catch(error => console.error('Erreur lors de la modification de la question ', error))
        }
    },
    emits: ['remove']
};
</script>