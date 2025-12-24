<script setup>
import { reactive, ref } from 'vue'

const emit = defineEmits(['submit'])

const form = reactive({
  full_name: '',
  email: '',
  phone: '',
  line1: '',
  line2: '',
  city: '',
  state: '',
  postal_code: '',
  country: 'US',
})

const submitting = ref(false)
const error = ref('')

const handleSubmit = async () => {
  error.value = ''
  submitting.value = true
  try {
    // Emit the payload to parent; parent can POST to backend
    console.log('Submitting address:', form)
    emit('submit', { ...form })
  } catch (err) {
    error.value = err?.message || 'Unable to submit address.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form class="address-form" @submit.prevent="handleSubmit">
    <header class="form-head">
      <div>
        <p class="eyebrow">Delivery</p>
        <h3>Shipping address</h3>
      </div>
      <button class="btn primary" type="submit" :disabled="submitting">
        {{ submitting ? 'Saving…' : 'Save address' }}
      </button>
    </header>

    <div class="grid two">
      <label class="field">
        <span>Full name</span>
        <input v-model.trim="form.full_name" required autocomplete="name" />
      </label>
      <label class="field">
        <span>Email</span>
        <input v-model.trim="form.email" type="email" required autocomplete="email" />
      </label>
    </div>

    <div class="grid two">
      <label class="field">
        <span>Phone</span>
        <input v-model.trim="form.phone" type="tel" autocomplete="tel" />
      </label>
      <label class="field">
        <span>Address line 1</span>
        <input v-model.trim="form.line1" required autocomplete="address-line1" />
      </label>
    </div>

    <label class="field">
      <span>Address line 2</span>
      <input v-model.trim="form.line2" autocomplete="address-line2" />
    </label>

    <div class="grid three">
      <label class="field">
        <span>City</span>
        <input v-model.trim="form.city" required autocomplete="address-level2" />
      </label>
      <label class="field">
        <span>State</span>
        <input v-model.trim="form.state" required autocomplete="address-level1" />
      </label>
      <label class="field">
        <span>Postal code</span>
        <input v-model.trim="form.postal_code" required autocomplete="postal-code" />
      </label>
    </div>

    <label class="field">
      <span>Country</span>
      <input v-model.trim="form.country" required autocomplete="country" />
    </label>

    <p v-if="error" class="status error">{{ error }}</p>
  </form>
</template>

<style scoped>
.address-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
}

.form-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  margin: 0;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  color: #334155;
}

.field input {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: #fff;
  transition: border-color 120ms ease, box-shadow 120ms ease;
}

.field input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
}

.grid.two {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}

.grid.three {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
}

.btn.primary {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 10px 14px;
  background: #2563eb;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.16);
}

.btn.primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.status.error {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #fca5a5;
  background: #fef2f2;
  color: #b91c1c;
}
</style>
