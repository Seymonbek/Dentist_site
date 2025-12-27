document.addEventListener('DOMContentLoaded', function() {
    const departmentSelect = document.querySelector('select[name="department"]');
    const doctorSelect = document.querySelector('select[name="doctor"]');
    const dateInput = document.querySelector('input[name="appointment_date"]');
    const timeSelect = document.querySelector('select[name="appointment_time"]');

    // 1. Bo'lim tanlanganda shifokorlarni yuklash
    if (departmentSelect) {
        departmentSelect.addEventListener('change', function() {
            const departmentId = this.value;
            doctorSelect.innerHTML = '<option value="">Shifokorni tanlang</option>';

            if (departmentId) {
                fetch(`/ajax/load-doctors/?department_id=${departmentId}`)
                    .then(res => res.json())
                    .then(data => {
                        data.forEach(doctor => {
                            const option = document.createElement('option');
                            option.value = doctor.id;
                            option.textContent = doctor.name;
                            doctorSelect.appendChild(option);
                        });
                    });
            }
        });
    }

    // 2. Bo'sh vaqtlarni yuklash funksiyasi
    function updateAvailableTimes() {
        const doctorId = doctorSelect.value;
        const date = dateInput.value;

        if (doctorId && date) {
            // URL manzili urls.py dagi bilan bir xil bo'lishi kerak
            fetch(`/ajax/get-available-times/?doctor_id=${doctorId}&date=${date}`)
                .then(res => res.json())
                .then(data => {
                    timeSelect.innerHTML = '<option value="">Vaqtni tanlang</option>';
                    if (data.available_slots) {
                        data.available_slots.forEach(slot => {
                            const option = document.createElement('option');
                            option.value = slot;
                            option.textContent = slot;
                            timeSelect.appendChild(option);
                        });
                    }
                });
        }
    }

    if (doctorSelect && dateInput) {
        doctorSelect.addEventListener('change', updateAvailableTimes);
        dateInput.addEventListener('change', updateAvailableTimes);
    }
});
