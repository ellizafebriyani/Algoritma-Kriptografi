// Function to submit form safely
function submitAll() {
    document.getElementById('upload').submit();
}

// This function is needed for the hill.html page
function validateAndSubmit() {
    // Get matrix size
    const matrixSize = document.querySelector('input[name="matrix-size"]:checked').value;
    const size = parseInt(matrixSize);
    const keyInputs = [];
    let isValid = true;
    let errorMessage = "";
    
    // Get all key values
    for (let i = 0; i < size; i++) {
        const inputElement = document.querySelector(`input[name="key_${i}"]`);
        if (!inputElement || !inputElement.value.trim()) {
            errorMessage = "Semua input matriks harus diisi.";
            isValid = false;
            break;
        }
        keyInputs.push(inputElement.value);
    }
    
    // Validate format if all inputs are filled
    if (isValid) {
        for (let i = 0; i < keyInputs.length; i++) {
            const values = keyInputs[i].split(',');
            
            // Check correct number of values
            if (values.length !== size) {
                errorMessage = `Baris ${i+1} harus berisi tepat ${size} angka yang dipisahkan koma.`;
                isValid = false;
                break;
            }
            
            // Check all values are numbers
            for (let j = 0; j < values.length; j++) {
                if (isNaN(parseInt(values[j]))) {
                    errorMessage = `Format input tidak valid pada baris ${i+1}. Masukkan angka yang dipisahkan koma.`;
                    isValid = false;
                    break;
                }
            }
            
            if (!isValid) break;
        }
    }
    
    // Show error or submit form
    if (!isValid) {
        showWarning(errorMessage);
    } else {
        document.getElementById('upload').submit();
    }
}

// Show warning message
function showWarning(message) {
    // Create warning if it doesn't exist
    let warningElement = document.querySelector('.warning-message');
    if (!warningElement) {
        warningElement = document.createElement('div');
        warningElement.className = 'warning-message';
        warningElement.style.color = 'red';
        warningElement.style.marginTop = '10px';
        
        const icon = document.createElement('i');
        icon.className = 'fas fa-exclamation-triangle';
        warningElement.appendChild(icon);
        
        const text = document.createTextNode(' ' + message);
        warningElement.appendChild(text);
        
        // Find where to insert the warning message
        const inputKeyWrapper = document.querySelector('.input-key-wrapper');
        if (inputKeyWrapper) {
            const container = inputKeyWrapper.parentNode;
            container.appendChild(warningElement);
        }
    } else {
        // Update existing warning
        warningElement.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + message;
        warningElement.style.display = 'block';
    }
}

// Adjust matrix inputs based on selected size
function adjustMatrixSize(size) {
    const matrixInputs = document.getElementById('matrix-inputs');
    if (!matrixInputs) return;
    
    // Store existing values
    const values = [];
    const inputs = matrixInputs.querySelectorAll('input');
    for (let i = 0; i < inputs.length && i < size; i++) {
        values[i] = inputs[i].value;
    }
    
    // Clear existing inputs
    matrixInputs.innerHTML = '';
    
    // Create new inputs based on size
    for (let i = 0; i < size; i++) {
        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'key_' + i;
        input.value = values[i] || '';
        
        if (size === 2) {
            input.placeholder = `Format: ${i === 0 ? 'a,b' : 'c,d'} (tanpa spasi)`;
        } else {
            input.placeholder = `Format: ${i === 0 ? 'a,b,c' : i === 1 ? 'd,e,f' : 'g,h,i'} (tanpa spasi)`;
        }
        
        matrixInputs.appendChild(input);
    }
}