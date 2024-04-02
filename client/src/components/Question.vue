<template>
    <div class="card">
        <div class="card-header">
            <input v-if="editing" type="text" v-model="editText" @blur="doneEdit" @keyup.enter="doneEdit">
            <span v-else @dblclick="edit">{{ editText }}</span>

        </div>
        <div class="card-body">
            <ul>
                <li v-for="(choice, index) in choices" :key="choice">
                    <input v-if="editingChoiceIndex === index" type="text" v-model="editChoiceText" @blur="doneEditChoice(index)" @keyup.enter="doneEditChoice(index)">
                    <span v-else>{{ choice }}</span>
                    <button class="btn btn-primary" @click="editChoice(index)">Edit</button>
                </li>
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
            editText: this.question.title,
            editingChoiceIndex: -1,
            editChoiceText: ''
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
                body: JSON.stringify({ title, choices: this.choices})
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Question modifiée')
                    } else {
                        console.error('Erreur lors de la modification de la question')
                    }
                })
                .catch(error => console.error('Erreur lors de la modification de la question ', error))
        },
        editChoice(index) {
            this.editingChoiceIndex = index;
            this.editChoiceText = this.choices[index];
        },
        doneEditChoice(index) {
            this.choices.splice(index, 1, this.editChoiceText);
            this.editQuestion(this.question.id, this.editText);
            this.editingChoiceIndex = -1;
        },
    },
    emits: ['remove']
};
</script>