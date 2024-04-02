<script>

import Questionnaire from './components/Questionnaire.vue'

export default {

  data(){
    return {
      questionnaires: [],
      questionnaireName: ''
    }
  },
  mounted(){
    this.getQuestionnaires()
  },
  methods: {
    getQuestionnaires(){
      fetch('http://127.0.0.1:5000/questionnaires')
      .then(response => response.json())
      .then(data => {
        this.questionnaires = data.questionnaires
      })
      .catch(error => console.error('Erreur lors de la récuperation des questionnaires ', error))
    },
    createQuestionnaire(){
      fetch('http://127.0.0.1:5000/questionnaires', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.questionnaireName
        })
      })
      .then(response => {
        if (response.ok) {
          console.log('Questionnaire ajouté')
          this.getQuestionnaires()
          this.questionnaireName = ''
        } else {
          console.error('Erreur lors de l\'ajout du questionnaire')
        }
      })
    },
    removeQuestionnaire(id){
      // Suppression des questions du questionnaire
      fetch(`http://127.0.0.1:5000//questions/questionnaire/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (response.ok) {
          // Suppression du questionnaire
          fetch(`http://127.0.0.1:5000/questionnaires/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
          })
          .then(response => {
            if (response.ok) {
              console.log('Questionnaire supprimé')
              this.getQuestionnaires()
            } else {
              console.error('Erreur lors de la suppression du questionnaire')
            }
          })
          .catch(error => console.error('Erreur lors de la suppression du questionnaire ', error))
        } else {
          console.error('Erreur lors de la suppression des questions du questionnaire')
        }
      })
      .catch(error => console.error('Erreur lors de la suppression des questions du questionnaire ', error))
    },
  },

  components: {
    Questionnaire
  }
}

</script>

<template>
<div>
  <h1>Mes questionnaires</h1>
  <div class="addQestionnaire">
    <input type="text" placeholder="Nom du questionnaire" required v-model="questionnaireName">
    <input type="button" value="Ajouter" class="btn btn-success" @click="createQuestionnaire">
  </div>
  <ul>
    <li class="nomQuestionnaire" v-for="questionnaire in questionnaires" :key="questionnaire.id">
      <div class="card">
        <Questionnaire :questionnaire="questionnaire" @remove="removeQuestionnaire"/>
      </div>
    </li>
  </ul>
</div>

</template>

<style scoped>
  .addQestionnaire {
    margin-bottom: 20px;
  }
  .addQestionnaire input[type="text"] {
    margin-right: 10px;
  }
  .addQestionnaire input[type="button"] {
    margin-left: 10px;
  }
  .card {
    margin-bottom: 40px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
</style>
