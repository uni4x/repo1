// app/reservation/static/js/reservation.js

document.addEventListener('DOMContentLoaded', function() {
    // Hide the new and edit forms initially
    document.getElementById('new_form').style.display = 'none';
    document.getElementById('edit_form').style.display = 'none';

    // Show new reservation form
    document.querySelector('.button').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('new_form').style.display = 'flex';
        document.getElementById('edit_form').style.display = 'none';
    });

    // Handle room search button click for new reservation form
    document.getElementById('search_rooms_button').addEventListener('click', function() {
        const checkinDate = document.getElementById('new_checkin_date').value;
        const checkoutDate = document.getElementById('new_checkout_date').value;
        
        if (!checkinDate || !checkoutDate) {
            alert('チェックイン日とチェックアウト日を選択してください。');
            return;
        }

        fetch('/reservation/update_room_choices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // CSRFトークンをヘッダーに追加
            },
            body: JSON.stringify({ checkin_date: checkinDate, checkout_date: checkoutDate })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching room data:', data.error);
                return;
            }
            const roomSelect = document.getElementById('new_room_id');
            roomSelect.innerHTML = '';  // Clear current options
            data.rooms.forEach(room => {
                const option = document.createElement('option');
                option.value = room.id;
                option.textContent = room.room_number;
                roomSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching room data:', error));
    });

    // Handle room search button click for edit reservation form
    document.getElementById('edit_search_rooms_button').addEventListener('click', function() {
        const checkinDate = document.getElementById('edit_checkin_date').value;
        const checkoutDate = document.getElementById('edit_checkout_date').value;
        
        if (!checkinDate || !checkoutDate) {
            alert('チェックイン日とチェックアウト日を選択してください。');
            return;
        }

        fetch('/reservation/update_room_choices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // CSRFトークンをヘッダーに追加
            },
            body: JSON.stringify({ checkin_date: checkinDate, checkout_date: checkoutDate })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching room data:', data.error);
                return;
            }
            const roomSelect = document.getElementById('edit_room_id');
            roomSelect.innerHTML = '';  // Clear current options
            data.rooms.forEach(room => {
                const option = document.createElement('option');
                option.value = room.id;
                option.textContent = room.room_number;
                roomSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching room data:', error));
    });
});


// Handle edit button click
document.querySelectorAll('a.edit-button').forEach(function(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const baseUrl = this.getAttribute('href');
        const id = baseUrl.split('/')[baseUrl.split('/').length - 1];
        const urlWithMode = baseUrl + '?mode=json';

        fetch(urlWithMode)
            .then(response => response.json())
            .then(data => {
                const editForm = document.getElementById('edit_form');
                if (editForm) {
                    const checkinDate = new Date(data.checkin_date);
                    const checkoutDate = new Date(data.checkout_date);

                    // 日付を YYYY-MM-DD 形式にフォーマットする関数
                    const formatDate = (date) => {
                        const year = date.getFullYear();
                        const month = String(date.getMonth() + 1).padStart(2, '0'); // 月を2桁にフォーマット
                        const day = String(date.getDate()).padStart(2, '0'); // 日を2桁にフォーマット
                        return `${year}-${month}-${day}`;
                    };

                    document.getElementById('edit_checkin_date').value = formatDate(checkinDate) || '';
                    document.getElementById('edit_checkout_date').value = formatDate(checkoutDate) || '';
                    document.getElementById('edit_customer_id').value = data.customer_id || '';
                    document.getElementById('edit_room_id').value = data.room_id || '';
                    document.getElementById('edit_payment_type').value = data.payment_type || '';
                    document.getElementById('edit_payment_status').value = data.payment_status || '';
                    document.getElementById('edit_number_of_guests').value = data.number_of_guests || '';
                    document.getElementById('edit_status').value = data.status || '';

                    editForm.action = baseUrl;
                    editForm.style.display = 'flex';
                    document.getElementById('new_form').style.display = 'none';
                    history.pushState(null, null, baseUrl);
                }
            })
            .catch(error => console.error('Error loading the reservation data:', error));
    });
});
