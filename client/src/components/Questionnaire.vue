<template>
    <div class="container">
        <input v-if="editing" type="text" v-model="editText" @blur="doneEdit" @keyup.enter="doneEdit">
        <h2 v-else @dblclick="edit">{{ editText }}</h2>
        <input type="button" class="btn btn-danger" value="SUPPRIMER" @click="removeQuestionnaire">
        <form @submit.prevent="addQuestion">
            <div class="form-group">
                <input type="text" class="form-control" placeholder="Intitulé de la question" required v-model="newQuestion.title">
            </div>
            <div class="form-group">
                <select class="form-control" required v-model="newQuestion.type">
                    <option value="question_simple">Question Simple</option>
                    <option value="question_multiple">Question Multiple</option>
                </select>
            </div>
            <div class="form-group">
                <input type="text" class="form-control" placeholder="Choix 1" required v-model="newQuestion.first_choix">
            </div>
            <div class="form-group">
                <input type="text" class="form-control" placeholder="Choix 2" required v-model="newQuestion.second_choix">
            </div>
            <div class="form-group" v-if="newQuestion.type === 'question_multiple'">
                <input type="text" class="form-control" placeholder="Choix 3 (si multiple)" v-model="newQuestion.third_choix">
            </div>
            <div class="form-group" v-if="newQuestion.type === 'question_multiple'">
                <input type="text" class="form-control" placeholder="Choix 4 (si multiple)" v-model="newQuestion.fourth_choix">
            </div>
            <input type="submit" class="btn btn-success" value="Ajouter question">
        </form>

        <ul>
            <li v-for="question in questions" :key="question.id">
                <Question :question="question" @remove="removeQuestion"/>
            </li>
        </ul>
    </div>
</template>

<script>
import Question from './Question.vue'

export default {
    props: {
        questionnaire: Object
    },
    components: {
        Question
    },
    data() {
        return {
            questions: [],
            editing: false,
            editText: this.questionnaire.name,
            newQuestion: {
                title: '',
                type: 'question_simple',
                first_choix: '',
                second_choix: '',
                third_choix: '',
                fourth_choix: ''
            }
        };
    },
    methods: {
        edit: function() {
            this.editing = true;
        },
        doneEdit: function() {
            this.editing = false;
            this.$emit('edit', this.questionnaire.id, this.editText);
            this.editQuestionnaire(this.questionnaire.id, this.editText)
        },
        removeQuestionnaire: function() {
            this.$emit('remove', this.questionnaire.id);
        },
        editQuestionnaire(id, name) {
            fetch(`http://127.0.0.1:5000/questionnaires/${this.questionnaire.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: name })
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Questionnaire modifié')
                    } else {
                        console.error('Erreur lors de la modification du questionnaire')
                    }
                })
                .catch(error => console.error('Erreur lors de la modification du questionnaire ', error))

        },
        getQuestions() {
            fetch(`http://127.0.0.1:5000/questionnaires/${this.questionnaire.id}/questions`,)
                .then(response => response.json())
                .then(data => {
                    this.questions = data.questions
                })
                .catch(error => console.error('Erreur lors de la récupération des questions ', error))
        },
        removeQuestion(id) {
            fetch(`http://127.0.0.1:5000//questions/${id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (response.ok) {
                        this.getQuestions()
                    } else {
                        console.error('Erreur lors de la suppression de la question')
                    }
                })
                .catch(error => console.error('Erreur lors de la suppression de la question ', error))
        },
        addQuestion() {
            fetch(`http://127.0.0.1:5000/questions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        title: this.newQuestion.title,
                        type: this.newQuestion.type,
                        first_choix: this.newQuestion.first_choix,
                        second_choix: this.newQuestion.second_choix,
                        third_choix: this.newQuestion.third_choix,
                        fourth_choix: this.newQuestion.fourth_choix,
                        questionnaire_id: this.questionnaire.id
                    }
                )
            })
                .then(response => {
                    if (response.ok) {
                        this.getQuestions()
                        this.newQuestion = {
                            title: '',
                            type: 'question_simple',
                            first_choix: '',
                            second_choix: '',
                            third_choix: '',
                            fourth_choix: ''
                        }
                    } else {
                        console.error('Erreur lors de l\'ajout de la question')
                    }
                })
                .catch(error => console.error('Erreur lors de l\'ajout de la question ', error))
        }
    },
    mounted() {
        this.getQuestions()
    }
}
</script>

<style scoped>
.container {
    margin-top: 20px;
}

.btn {
    margin: 20px;
}
</style>