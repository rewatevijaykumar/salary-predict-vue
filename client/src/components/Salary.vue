<template>
    <div class="container">
        <div class="row">
            <div class="col">

                <b-card
                border-variant="success"
                header="Salary Prediction"
                header-text-variant="white"
                header-bg-variant="success"
                header-class="font-weight-bold h4"
                bg-variant="light"
                align="center">
                    <b-card-text>
                <b-form @submit="onSubmit" @reset="onReset">
                <b-form-group
                    id="form-experience-group"
                    label-cols-md="3"
                    label="Experience:"
                    label-align-md="right"
                    label-size="lg"
                    label-for="form-experience-input"
                    label-class="font-weight-bold pt-0"

                >
                <b-form-input
                id="form-experience-input"
                type="text"
                v-model="addDetailForm.exp"
                required
                placeholder="Enter your experience"></b-form-input>
                </b-form-group>
                <b-form-group
                    id="form-testscore-group"
                    label-cols-md="3"
                    label="Test Score:"
                    label-align-md="right"
                    label-size="lg"
                    label-for="form-testscore-input"
                    label-class="font-weight-bold pt-0"
                >
                <b-form-input
                id="form-testscore-input"
                type="text"
                v-model="addDetailForm.test"
                required
                placeholder="Enter your test score out of 10"></b-form-input>
                </b-form-group>
                <b-form-group
                    id="form-interviewscore-group"
                    label-cols-md="3"
                    label="Interview Score:"
                    label-align-md="right"
                    label-size="lg"
                    label-for="form-interviewscore-input"
                    label-class="font-weight-bold pt-0"
                >
                <b-form-input
                id="form-interviewscore-input"
                type="text"
                v-model="addDetailForm.inter"
                required
                placeholder="Enter your interview score out of 10"></b-form-input>
                </b-form-group>

                <b-button class="btn btn-info btn-block" type="submit">
                <h4 class="m-0">Submit</h4></b-button>
                <b-button class="btn btn-danger btn-block"
                type="reset" ><h4 class="m-0">Reset</h4></b-button>

                </b-form>
                </b-card-text>
                </b-card>
                <br><br>
                <b-card v-if="predict"
                border-variant="success"
                header-bg-variant="success"
                header="ESTIMATED SALARY"
                header-class="font-weight-bold h4"
                bg-variant="light"
                text-variant="white">
                <input type="text"
                       class="form-control"
                       v-model="salary"
                       required>

                </b-card>

            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      salary: '',
      addDetailForm: {
        exp: '',
        test: '',
        inter: '',
      },
      predict: false,
    };
  },
  methods: {
    addDetails(payload) {
      const path = '/salary';
      axios.post(path, payload)
        .then((res) => {
          this.salary = res.data.salary;
          this.predict = true;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.log(error);
        });
    },
    initForm() {
      this.addDetailForm.exp = '';
      this.addDetailForm.test = '';
      this.addDetailForm.inter = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        exp: this.addDetailForm.exp,
        test: this.addDetailForm.test,
        inter: this.addDetailForm.inter,
      };
      this.addDetails(payload);
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
    created() {
      this.onReset();
    },
  },
};
</script>

<style>

</style>
