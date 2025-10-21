document.addEventListener("DOMContentLoaded", function() {
    
    const modal = document.getElementById("feedback-modal");
    const openBtn = document.getElementById("open-feedback-btn");
    const closeBtn = document.getElementsByClassName("close-modal")[0]; 
    const form = document.getElementById("feedback-form");
    const successMessageDiv = document.getElementById("feedback-success-message");

    

    function clearErrors() {
        
        if (document.getElementById('error-nome')) {
            document.getElementById('error-nome').innerText = '';
        }
        if (document.getElementById('error-email')) {
            document.getElementById('error-email').innerText = '';
        }
        if (document.getElementById('error-mensagem')) {
            document.getElementById('error-mensagem').innerText = '';
        }
    }

    function resetModal() {
        if (form) {
            form.reset(); 
            form.style.display = 'block'; 
        }
        if (successMessageDiv) {
            successMessageDiv.style.display = 'none'; 
            successMessageDiv.innerText = '';
        }
        clearErrors();
    }


    if (openBtn) {
        // ✅ MUDANÇA AQUI:
        openBtn.onclick = function(event) { // 1. Adicionado "event"
            event.preventDefault();         // 2. Adicionado "preventDefault()"
            
            if (modal) {
                modal.style.display = "block";
                resetModal(); 
            }
        }
    }

    if (closeBtn) {
        closeBtn.onclick = function() {
            if (modal) {
                modal.style.display = "none";
            }
        }
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); 
            clearErrors(); 

            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', 
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    
                    form.style.display = 'none'; 
                    successMessageDiv.innerText = data.message; 
                    successMessageDiv.style.display = 'block'; 
                    
                    setTimeout(() => {
                        if (modal) {
                            modal.style.display = "none";
                        }
                    }, 3000);

                } else if (data.errors) {
                    for (const field in data.errors) {
                        const errorMsg = data.errors[field][0].message; 
                        const errorDiv = document.getElementById(`error-${field}`);
                        if (errorDiv) {
                            errorDiv.innerText = errorMsg;
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Erro no fetch:', error);
                alert('Ocorreu um erro inesperado. Tente novamente.');
            });
        });
    }

});