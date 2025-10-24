// static/js/script.js (Nâng cấp hỗ trợ nhiều khối lớp + Chứng nhận)
// ĐÃ BỎ HIỆU ỨNG PHÁO HOA (CONFETTI)
// ĐÃ THÊM NÚT "VỀ BẢNG ĐIỀU KHIỂN"

const dom = {
    controlPanel: document.getElementById('control-panel'),
    displayArea: document.getElementById('display-area'),
    gradeSelect: document.getElementById('grade-select'),
    unitSelect: document.getElementById('unit-select'),
    
    // MỚI: Thêm input cho tên và lớp
    studentNameInput: document.getElementById('student-name'),
    studentClassInput: document.getElementById('student-class'),
    
    questionTypesContainer: document.getElementById('question-types'),
    generateBtn: document.getElementById('generate-btn'),
    
    // MỚI: Nút tạo bài tổng hợp
    generateComprehensiveBtn: document.getElementById('generate-comprehensive-btn'),
    
    placeholder: document.getElementById('placeholder'),
    loading: document.getElementById('loading'),
    loadingText: document.getElementById('loading-text'),
    errorMessage: document.getElementById('error-message'),
    errorText: document.getElementById('error-text'),
    
    quizWrapper: document.getElementById('quiz-wrapper'),
    quizBody: document.getElementById('quiz-body'),
    submitBtn: document.getElementById('submit-btn'),
    printBtn: document.getElementById('print-btn'),
    
    resultWrapper: document.getElementById('result-wrapper'),
    score: document.getElementById('score'),
    resultBody: document.getElementById('result-body'),
    resetBtn: document.getElementById('reset-btn'),
    backToPanelBtn: document.getElementById('back-to-panel-btn'), // <-- ĐÃ THÊM
    resultImageContainer: document.getElementById('result-image-container'),
    resultFeedback: document.getElementById('result-feedback'),
    // confettiContainer: (ĐÃ BỎ)
    
    // MỚI: Các thành phần của Chứng nhận
    certificateWrapper: document.getElementById('certificate-wrapper'),
    certificateName: document.getElementById('certificate-name'),
    certificateClass: document.getElementById('certificate-class'),
    certificateUnit: document.getElementById('certificate-unit'),
    certificateDate: document.getElementById('certificate-date'),
    retakeQuizBtn: document.getElementById('retake-quiz-btn') // Nút làm lại bài trên chứng nhận
};

let generatedQuestions = [];
let totalQuestionsInQuiz = 0;
let isComprehensiveTest = false; // MỚI: Cờ để biết đây là bài tổng hợp

// ==========================================================
// CƠ SỞ DỮ LIỆU CHƯƠNG TRÌNH HỌC (MỚI)
// ĐÃ CẬP NHẬT ĐẦY ĐỦ LỚP 1, 2, 3, 4, 5
// ==========================================================
const curriculumData = {
    "1": { // Lớp 1
        units: [
            // === TÊN UNIT LỚP 1 ĐÃ ĐƯỢC CẬP NHẬT ===
            "Unit 1: My first day at school",
            "Unit 2: My school things",
            "Unit 3: My toys",
            "Unit 4: My body",
            "Unit 5: My pets",
            "Unit 6: My home",
            "Unit 7: My family",
            "Unit 8: My clothes",
            "Unit 9: My colours",
            "Unit 10: My hobbies",
            "Unit 11: My family", // Sách 2
            "Unit 12: My house",
            "Unit 13: My room",
            "Unit 14: My birthday",
            "Unit 15: My activities",
            "Unit 16: My pets" // (Sách 2, Unit 16)
        ],
        questionTypes: [
            // === DANH SÁCH DẠNG BÀI LỚP 1 ĐÃ ĐƯỢC CẬP NHẬT ===
            { value: 'mcq', label: 'Trắc nghiệm', checked: true, count: 5, max: 10 },
            { value: 'fill', label: 'Điền từ', checked: true, count: 5, max: 10 },
            { value: 'scramble', label: 'Sắp xếp câu', checked: false, count: 3, max: 5 },
            { value: 'match', label: 'Nối từ', checked: false, count: 1, max: 2 },
            { value: 'writing', label: 'Viết lại câu', checked: false, count: 2, max: 5 }, // ĐÃ THÊM
            { value: 'reading', label: 'Đọc hiểu', checked: false, count: 1, max: 3 }  // ĐÃ THÊM
        ]
    },
    "2": { // Lớp 2
        units: [
            "Unit 1: At my birthday party",
            "Unit 2: In the backyard",
            "Unit 3: At the seaside",
            "Unit 4: In the countryside",
            "Unit 5: In the classroom",
            "Unit 6: On the farm",
            "Unit 7: In the kitchen",
            "Unit 8: In the village",
            "Unit 9: In the grocery store",
            "Unit 10: At the zoo",
            "Unit 11: In the playground",
            "Unit 12: At the café",
            "Unit 13: In the maths class",
            "Unit 14: At home",
            "Unit 15: In the clothes shop",
            "Unit 16: At the campsite"
        ],
        questionTypes: [
            { value: 'mcq', label: 'Trắc nghiệm', checked: true, count: 5, max: 10 },
            { value: 'fill', label: 'Điền từ', checked: true, count: 5, max: 10 },
            { value: 'scramble', label: 'Sắp xếp câu', checked: false, count: 3, max: 5 },
            { value: 'match', label: 'Nối từ', checked: false, count: 1, max: 2 },
            { value: 'writing', label: 'Viết lại câu', checked: false, count: 2, max: 5 },
            { value: 'reading', label: 'Đọc hiểu', checked: false, count: 1, max: 3 }
        ]
    },
    "3": { // Lớp 3
        units: [
            "Unit 1: Hello",
            "Unit 2: Our names",
            "Unit 3: Our friends",
            "Unit 4: Our bodies",
            "Unit 5: My hobbies",
            "Unit 6: Our school",
            "Unit 7: Classroom instructions",
            "Unit 8: My school things",
            "Unit 9: Colours",
            "Unit 10: Break time activities",
            "Unit 11: My family",
            "Unit 12: Jobs",
            "Unit 13: My house",
            "Unit 14: My bedroom",
            "Unit 15: At the dining table",
            "Unit 16: My pets",
            "Unit 17: Our toys",
            "Unit 18: Playing and doing",
            "Unit 19: Outdoor activities",
            "Unit 20: At the zoo"
        ],
        questionTypes: [
            { value: 'mcq', label: 'Trắc nghiệm', checked: true, count: 5, max: 10 },
            { value: 'fill', label: 'Điền từ', checked: true, count: 5, max: 10 },
            { value: 'scramble', label: 'Sắp xếp câu', checked: false, count: 3, max: 5 },
            { value: 'match', label: 'Nối từ', checked: false, count: 1, max: 2 },
            { value: 'writing', label: 'Viết lại câu', checked: false, count: 2, max: 5 },
            { value: 'reading', label: 'Đọc hiểu', checked: false, count: 1, max: 3 }
        ]
    },
    "4": { // Lớp 4
        units: [
            "Unit 1: My friends",
            "Unit 2: Time and daily routines",
            "Unit 3: My week",
            "Unit 4: My birthday party",
            "Unit 5: Things we can do",
            "Unit 6: Our school facilities",
            "Unit 7: Our timetables",
            "Unit 8: My favourite subjects",
            "Unit 9: Our sports day",
            "Unit 10: Our summer holidays",
            "Unit 11: My home",
            "Unit 12: Jobs",
            "Unit 13: Appearance",
            "Unit 14: Daily activities",
            "Unit 15: My family's weekends",
            "Unit 16: Weather",
            "Unit 17: In the city",
            "Unit 18: At the shopping centre",
            "Unit 19: The animal world",
            "Unit 20: At summer camp"
        ],
        questionTypes: [
            { value: 'mcq', label: 'Trắc nghiệm', checked: true, count: 5, max: 10 },
            { value: 'fill', label: 'Điền từ', checked: true, count: 5, max: 10 },
            { value: 'scramble', label: 'Sắp xếp câu', checked: false, count: 3, max: 5 },
            { value: 'match', label: 'Nối từ', checked: false, count: 1, max: 2 },
            { value: 'writing', label: 'Viết lại câu', checked: false, count: 2, max: 5 },
            { value: 'reading', label: 'Đọc hiểu', checked: false, count: 1, max: 3 }
        ]
    },
    "5": { // Lớp 5
        units: [
            "Unit 1: All about me!",
            "Unit 2: Our homes",
            "Unit 3: My foreign friends",
            "Unit 4: Our free-time activities",
            "Unit 5: My future job",
            "Unit 6: Our school rooms",
            "Unit 7: Our favourite school activities",
            "Unit 8: In our classroom",
            "Unit 9: Our outdoor activities",
            "Unit 10: Our school trip"
        ],
        questionTypes: [
            { value: 'mcq', label: 'Trắc nghiệm', checked: true, count: 5, max: 10 },
            { value: 'fill', label: 'Điền từ', checked: true, count: 5, max: 10 },
            { value: 'scramble', label: 'Sắp xếp câu', checked: false, count: 3, max: 5 },
            { value: 'match', label: 'Nối từ', checked: false, count: 1, max: 2 },
            { value: 'writing', label: 'Viết lại câu', checked: false, count: 2, max: 5 },
            { value: 'reading', label: 'Đọc hiểu', checked: false, count: 1, max: 3 }
        ]
    }
    // (Thêm khối lớp ... vào đây khi cần)
};
// ==========================================================

/**
 * MỚI: Cập nhật danh sách Unit dựa trên khối lớp đã chọn
 */
function populateUnitSelect() {
// ... (Giữ nguyên hàm này)
    const selectedGrade = dom.gradeSelect.value;
    const units = curriculumData[selectedGrade]?.units || [];
    
    if (units.length === 0) {
        dom.unitSelect.innerHTML = `<option value="">-- Vui lòng chọn khối lớp --</option>`;
        return;
    }
    
    dom.unitSelect.innerHTML = units.map(unit => `<option value="${unit}">${unit}</option>`).join('');
}

/**
 * CẬP NHẬT: Khởi tạo các tùy chọn dạng bài dựa trên khối lớp đã chọn
 */
function initializeQuestionTypes() {
// ... (Giữ nguyên hàm này)
    const selectedGrade = dom.gradeSelect.value;
    const questionTypeOptions = curriculumData[selectedGrade]?.questionTypes || [];

    let html = '';
    questionTypeOptions.forEach(opt => {
        const countValue = opt.count || 5;
        const maxCount = opt.max || 10;
        
        // Logic này giờ xử lý đúng cho cả Lớp 1 và Lớp 5
        const finalCount = opt.value === 'reading' ? (opt.count || 1) : countValue;
        const finalMax = opt.value === 'reading' ? (opt.max || 3) : maxCount;

        html += `
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border gap-x-2">
                <label class="flex items-center space-x-2 cursor-pointer grow">
                    <input type="checkbox" value="${opt.value}" data-type-checkbox ${opt.checked ? 'checked' : ''}>
                    <span>${opt.label}</span>
                </label>
                
                <select data-type-difficulty="${opt.value}" class="w-28 p-1 border border-gray-300 rounded-md text-center ${opt.checked ? '' : 'hidden'}">
                    <option value="Dễ">Dễ</option>
                    <option value="Trung bình" selected>Trung bình</option>
                    <option value="Khó">Khó</option>
                </select>
                
                <input type="number" value="${finalCount}" min="1" max="${finalMax}"
                       class="w-20 p-1 border border-gray-300 rounded-md text-center ${opt.checked ? '' : 'hidden'}"
                       data-type-count="${opt.value}">
            </div>
        `;
    });
    
    dom.questionTypesContainer.innerHTML = html;
    
    // Xóa listener cũ (nếu có) để tránh gọi nhiều lần
    const newContainer = dom.questionTypesContainer.cloneNode(true);
    dom.questionTypesContainer.parentNode.replaceChild(newContainer, dom.questionTypesContainer);
    dom.questionTypesContainer = newContainer;

    // Thêm listener mới
    dom.questionTypesContainer.addEventListener('change', (e) => {
        if (e.target.matches('[data-type-checkbox]')) {
            const countInput = dom.questionTypesContainer.querySelector(`[data-type-count="${e.target.value}"]`);
            const difficultySelect = dom.questionTypesContainer.querySelector(`[data-type-difficulty="${e.target.value}"]`);
            if (countInput && difficultySelect) {
                countInput.classList.toggle('hidden', !e.target.checked);
                difficultySelect.classList.toggle('hidden', !e.target.checked);
            }
        }
    });
}

/**
 * MỚI: Xử lý khi người dùng thay đổi khối lớp
 */
function handleGradeChange() {
// ... (Giữ nguyên hàm này)
    populateUnitSelect();
    initializeQuestionTypes();
}

/**
 * CẬP NHẬT: Gửi yêu cầu tạo bài (thêm `grade`)
 */
async function handleGenerate() {
    isComprehensiveTest = false; // Đặt cờ là bài test thường
    
    const selectedGrade = dom.gradeSelect.value;
    const selectedUnit = dom.unitSelect.value;
    const selectedTypes = [];
    const checkedBoxes = dom.questionTypesContainer.querySelectorAll('input[type="checkbox"]:checked');
    
    if (!selectedGrade || !selectedUnit) {
        showError("Vui lòng chọn khối lớp và unit.");
        return;
    }
    
    // MỚI: Yêu cầu nhập tên và lớp
    if (!dom.studentNameInput.value || !dom.studentClassInput.value) {
        showError("Vui lòng nhập tên học sinh và lớp trước khi tạo bài.");
        return;
    }

    checkedBoxes.forEach(box => {
        const type = box.value;
        const countInput = dom.questionTypesContainer.querySelector(`[data-type-count="${type}"]`);
        const difficultySelect = dom.questionTypesContainer.querySelector(`[data-type-difficulty="${type}"]`);
        const count = parseInt(countInput.value);
        const difficulty = difficultySelect.value;
        if (count > 0) {
            selectedTypes.push({ type, count, difficulty });
        }
    });

    if (selectedTypes.length === 0) {
        showError("Vui lòng chọn ít nhất một dạng bài.");
        return;
    }
    
    await startQuizGeneration(selectedGrade, selectedUnit, selectedTypes);
}

/**
 * MỚI: Xử lý tạo bài kiểm tra tổng hợp
 */
async function handleGenerateComprehensive() {
    isComprehensiveTest = true; // Đặt cờ là bài tổng hợp
    
    const selectedGrade = dom.gradeSelect.value;
    const selectedUnit = dom.unitSelect.value;
    
    if (!selectedGrade || !selectedUnit) {
        showError("Vui lòng chọn khối lớp và unit.");
        return;
    }
    
    // MỚI: Yêu cầu nhập tên và lớp
    if (!dom.studentNameInput.value || !dom.studentClassInput.value) {
        showError("Vui lòng nhập tên học sinh và lớp trước khi tạo bài.");
        return;
    }

    // Lấy danh sách các dạng bài được hỗ trợ cho khối lớp này
    const supportedTypes = (curriculumData[selectedGrade]?.questionTypes || []).map(qt => qt.value);

    // Cấu hình cố định cho bài tổng hợp
    const comprehensiveTypesConfig = [
        { type: 'mcq', count: 3, difficulty: 'Trung bình' },
        { type: 'fill', count: 3, difficulty: 'Trung bình' },
        { type: 'scramble', count: 3, difficulty: 'Trung bình' },
        { type: 'match', count: 3, difficulty: 'Trung bình' },
        { type: 'writing', count: 2, difficulty: 'Trung bình' },
        { type: 'reading', count: 1, difficulty: 'Trung bình' }
    ];
    
    // Lọc ra các dạng bài mà khối lớp đó hỗ trợ
    const selectedTypes = comprehensiveTypesConfig.filter(config => supportedTypes.includes(config.type));
    
    if (selectedTypes.length === 0) {
        showError("Khối lớp này không hỗ trợ dạng bài nào để tạo bài tổng hợp.");
        return;
    }

    await startQuizGeneration(selectedGrade, selectedUnit, selectedTypes, "AI đang tạo bài kiểm tra tổng hợp...");
}

/**
 * MỚI: Hàm chung để tạo bài, tránh lặp code
 */
async function startQuizGeneration(grade, unit, types, loadingMessage = 'AI đang tạo bài kiểm tra...') {
    setUIState('loading');
    dom.loadingText.textContent = loadingMessage;
    try {
        const result = await generateQuestions(grade, unit, types);
        generatedQuestions = result.questions;
        
        if (!generatedQuestions || generatedQuestions.length === 0) {
            throw new Error("AI không thể tạo câu hỏi. Vui lòng thử lại.");
        }
        
        displayQuiz(generatedQuestions);
        setUIState('quizWrapper');
        dom.controlPanel.classList.add('hidden'); // Ẩn control panel khi làm bài
    } catch (error) {
        showError(error.message);
    }
}

/**
 * MỚI: Hàm hiển thị lỗi
 */
function showError(message) {
    dom.errorText.textContent = `Lỗi: ${message}`;
    setUIState('errorMessage');
}


/**
 * CẬP NHẬT: Thêm `certificateWrapper` vào danh sách ẩn
 */
function setUIState(state) {
    ['placeholder', 'loading', 'errorMessage', 'quizWrapper', 'resultWrapper', 'certificateWrapper'].forEach(id => {
        if (dom[id]) dom[id].classList.add('hidden');
    });
    if (state && dom[state]) dom[state].classList.remove('hidden');
}

function shuffle(array) {
// ... (Giữ nguyên hàm này)
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

/**
 * CẬP NHẬT: Thêm `grade` vào request
 */
async function generateQuestions(grade, unit, types) {
// ... (Giữ nguyên hàm này)
    try {
        const response = await fetch('/generate-quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ grade, unit, types }), // Gửi cả 3 thông tin
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Lỗi từ server: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Lỗi khi tạo câu hỏi:", error);
        throw error;
    }
}

/**
 * CẬP NHẬT: Thêm `grade` vào request để AI biết cách giải thích
 */
async function getExplanation(question, userAnswer, correctAnswer) {
// ... (Giữ nguyên hàm này)
    const selectedGrade = dom.gradeSelect.value; // Lấy khối lớp hiện tại
    try {
        const response = await fetch('/get-explanation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ grade: selectedGrade, question, userAnswer, correctAnswer }),
        });
        if (!response.ok) throw new Error('Không thể lấy được giải thích từ server.');
        return await response.json();
    } catch (error) {
        console.error("Lỗi khi lấy giải thích:", error);
        return { explanation: "Rất tiếc, không thể tải giải thích lúc này." };
    }
}

function displayQuiz(questions) {
// ... (Giữ nguyên hàm này)
    let quizHTML = '';
    let questionCounter = 0;
    totalQuestionsInQuiz = 0;

    questions.forEach((q, index) => {
        quizHTML += `<div class="quiz-question p-4" id="q-container-${index}" data-type="${q.type}">`;
        
        switch (q.type) {
            case 'reading':
                questionCounter++;
                quizHTML += `<p class="mb-2"><b>Câu ${questionCounter}: Đọc đoạn văn sau và trả lời các câu hỏi bên dưới.</b></p>`;
                quizHTML += `<div class="passage bg-gray-50 p-4 rounded-lg border text-gray-700 mb-6">${q.passage.replace(/\n/g, '<br>')}</div>`;
                
                if (q.sub_questions && q.sub_questions.length > 0) {
                    quizHTML += `<div class="space-y-6">`;
                    q.sub_questions.forEach((sub_q, sub_index) => {
                        totalQuestionsInQuiz++;
                        quizHTML += `<div class="sub-question ml-4" id="q-container-${index}-${sub_index}">`;
                        quizHTML += `<p class="mb-3"><b>Câu ${questionCounter}.${sub_index + 1}:</b> ${sub_q.question}</p>`;

                        if (sub_q.type === 'true_false') {
                            quizHTML += `<div class="space-y-2 flex items-center gap-x-6">
                                            <label class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 cursor-pointer">
                                                <input type="radio" name="q${index}-${sub_index}" value="True" class="h-4 w-4">
                                                <span><i class="fas fa-check text-green-500"></i> True</span>
                                            </label>
                                            <label class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 cursor-pointer">
                                                <input type="radio" name="q${index}-${sub_index}" value="False" class="h-4 w-4">
                                                <span><i class="fas fa-times text-red-500"></i> False</span>
                                            </label>
                                         </div>`;
                        } else { // Giả định là 'mcq'
                            const shuffledOptions = sub_q.options ? shuffle([...sub_q.options]) : [];
                            quizHTML += `<div class="space-y-2">`;
                            shuffledOptions.forEach((opt, optIndex) => {
                                quizHTML += `<label class="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 cursor-pointer">
                                    <input type="radio" name="q${index}-${sub_index}" value="${opt}" class="h-4 w-4">
                                    <span><b>${String.fromCharCode(65 + optIndex)}.</b> ${opt}</span>
                                </label>`;
                            });
                            quizHTML += `</div>`;
                        }
                        quizHTML += `</div>`;
                    });
                    quizHTML += `</div>`;
                }
                break;
            
            default:
                questionCounter++;
                totalQuestionsInQuiz++;
                if (q.type === 'mcq') {
                    quizHTML += `<p class="mb-3"><b>Câu ${questionCounter}:</b> ${q.question}</p>`;
                    const shuffledOptions = q.options ? shuffle([...q.options]) : [];
                    quizHTML += `<div class="space-y-2">`;
                    shuffledOptions.forEach((opt, optIndex) => {
                        quizHTML += `<label class="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 cursor-pointer">
                            <input type="radio" name="q${index}" value="${opt}" class="h-4 w-4">
                            <span><b>${String.fromCharCode(65 + optIndex)}.</b> ${opt}</span>
                        </label>`;
                    });
                    quizHTML += `</div>`;
                } else if (q.type === 'fill') {
                     quizHTML += `<p class="mb-2"><b>Câu ${questionCounter}:</b> ${q.question.replace('___', '<input type="text" name="q'+index+'" class="border-b-2 border-gray-300 focus:border-blue-500 outline-none px-2 w-32 md:w-48">')}</p>`;
                } else if (q.type === 'scramble') {
                    quizHTML += `<p class="mb-2"><b>Câu ${questionCounter}:</b> Sắp xếp các từ sau: ${q.question}</p>
                                 <input type="text" name="q${index}" class="w-full mt-2 p-2 border rounded-lg" placeholder="Viết câu trả lời của bạn...">`;
                } else if (q.type === 'writing') {
                    quizHTML += `<p class="mb-2"><b>Câu ${questionCounter}:</b> ${q.question}</p>
                                 <textarea name="q${index}" class="w-full mt-2 p-2 border rounded-lg" rows="3" placeholder="Viết câu của bạn ở đây..."></textarea>`;
                } else if (q.type === 'match') {
                    quizHTML += `<p class="mb-2"><b>Câu ${questionCounter}:</b> ${q.question}</p>`;
                    if (q.pairs && q.pairs.length > 0) {
                        const leftCol = shuffle([...q.pairs]);
                        const rightCol = shuffle([...q.pairs]);
                        
                        // Tạo map đáp án đúng (ví dụ: { "book": "A", "pen": "B" })
                        const answerMap = {};
                        const rightColItems = rightCol.map((p, i) => ({ char: String.fromCharCode(65 + i), text: p.a }));
                        leftCol.forEach(leftPair => {
                            const correspondingRight = rightColItems.find(rightPair => rightPair.text === leftPair.a);
                            if (correspondingRight) {
                                answerMap[leftPair.q] = correspondingRight.char;
                            }
                        });

                        quizHTML += `<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                                        <div>
                                            <b>Cột A</b>
                                            <ul class="list-none space-y-2 mt-2">${leftCol.map((p, i) => `
                                                <li class="flex items-center">
                                                    <b>${i+1}.</b> ${p.q} 
                                                    <input type="text" name="q${index}-${i}" class="border-b-2 w-8 ml-2 text-center" maxlength="1" data-left-item="${p.q}">
                                                </li>`).join('')}
                                            </ul>
                                        </div>
                                        <div>
                                            <b>Cột B</b>
                                            <ul class="list-none space-y-2 mt-2">${rightColItems.map(item => `
                                                <li><b>${item.char}.</b> ${item.text}</li>`).join('')}
                                            </ul>
                                        </div>
                                     </div>`;
                        // Lưu map đáp án vào một element ẩn để chấm điểm
                        quizHTML += `<div class="hidden" data-match-map="${encodeURIComponent(JSON.stringify(answerMap))}"></div>`;
                    }
                }
                break;
        }
        quizHTML += `</div>`;
    });
    dom.quizBody.innerHTML = quizHTML;
}

function displayResults(results) {
// ... (Giữ nguyên hàm này)
    let resultHTML = '';
    let resultCounter = 0;
    let lastPassage = null;

    results.forEach((res) => {
        resultCounter++;
        if (res.passage && res.passage !== lastPassage) {
            resultHTML += `<div class="passage-result mt-6 mb-2 p-3 bg-gray-100 rounded-lg border">
                <p class="font-bold text-gray-800">Bài đọc hiểu:</p>
                <p class="text-sm text-gray-600 italic">"${res.passage.substring(0, 100)}..."</p>
            </div>`;
            lastPassage = res.passage;
        }

        const isCorrect = res.isCorrect;
        resultHTML += `<div class="result-item p-4 rounded-lg ${isCorrect ? 'correct bg-green-50' : 'incorrect bg-red-50'}">
            <div class="flex flex-col gap-y-1">
                <p class="font-semibold">${resultCounter}. ${res.question}</p>
                <p class="${isCorrect ? 'text-green-700' : 'text-red-700'}">${res.userAnswer || '<i>(chưa trả lời)</i>'}</p>
                ${!isCorrect ? `<p><span class="font-semibold text-gray-600">Đáp án đúng:</span> <span class="font-semibold text-green-800">${res.correctAnswer}</span></p>` : ''}
                ${!isCorrect ? `<div id="explanation-${resultCounter - 1}" class="p-2 bg-yellow-50 text-yellow-800 rounded-lg text-sm mt-2">AI đang giải thích...</div>` : ''}
            </div>
        </div>`;
    });
    dom.resultBody.innerHTML = resultHTML;
}

/**
 * CẬP NHẬT: Thay đổi ảnh GIF dựa trên điểm số
 */
function displayFeedback(score, total) {
// ... (Giữ nguyên hàm này)
    const scorePercent = total > 0 ? (score / total) * 100 : 0;
    
    let feedback = {};
    let resultImageUrl = '';

    if (scorePercent >= 80) {
        feedback = { title: "Xuất sắc! ✨", message: "Bạn đã làm rất tốt! Vốn từ vựng và ngữ pháp của bạn thực sự chắc chắn.", tip: "<b>Mẹo nhỏ:</b> Để thử thách bản thân, hãy thử dùng những từ vựng vừa học để đặt câu hoặc viết một đoạn văn ngắn." };
        resultImageUrl = 'https://i.gifer.com/YARz.gif'; // Ăn mừng
    } else if (scorePercent >= 50) {
        feedback = { title: "Cố gắng lên! 👍", message: "Kết quả rất tốt! Bạn đã nắm được phần lớn kiến thức quan trọng. Chỉ cần ôn lại một chút ở các câu sai là bạn sẽ tiến bộ rất nhanh.", tip: "<b>Mẹo nhỏ:</b> Hãy xem kỹ phần giải thích của AI cho các câu trả lời sai." };
        resultImageUrl = 'https://i.gifer.com/74b.gif'; // Vỗ tay
    } else {
        feedback = { title: "Đừng nản lòng! ❤️", message: "Không sao cả, học tập là một hành trình. Điều quan trọng là bạn đã nỗ lực làm bài.", tip: "<b>Mẹo nhỏ:</b> Sau khi xem lại đáp án, bạn hãy thử làm lại bài kiểm tra này một lần nữa." };
        resultImageUrl = 'https://i.gifer.com/6k6.gif'; // Động viên
    }
    dom.resultFeedback.innerHTML = `<h3 class="text-xl font-bold text-gray-800">${feedback.title}</h3><p class="text-gray-600 mt-1">${feedback.message}</p><p class="text-sm text-gray-500 mt-3">${feedback.tip}</p>`;
    
    dom.resultImageContainer.innerHTML = `<img src="${resultImageUrl}" alt="Kết quả bài làm" class="w-32 h-32 mx-auto rounded-full shadow-lg">`;
}

/**
 * MỚI: Hiển thị chứng nhận
 */
function displayCertificate(studentName, studentClass, unitName) {
    dom.certificateName.textContent = studentName;
    dom.certificateClass.textContent = studentClass;
    dom.certificateUnit.textContent = unitName;
    dom.certificateDate.textContent = new Date().toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

/**
 * CẬP NHẬT: Logic chấm điểm và hiển thị chứng nhận
 */
async function handleSubmit() {
    setUIState('loading');
    dom.loadingText.textContent = 'Đang chấm bài và tạo giải thích...';

    let score = 0;
    const results = [];
    
    // Hàm chuẩn hóa chuỗi để chấm điểm linh hoạt
    const normalize = (str) => {
        if (typeof str !== 'string') return '';
        return str.toLowerCase().replace(/[.,!?]/g, '').trim();
    };

    generatedQuestions.forEach((q, index) => {
        // ... (Logic chấm điểm giữ nguyên)
        const container = document.getElementById(`q-container-${index}`);
        
        if (q.type === 'reading' && q.sub_questions) {
            q.sub_questions.forEach((sub_q, sub_index) => {
                const subContainer = document.getElementById(`q-container-${index}-${sub_index}`);
                const checked = subContainer.querySelector('input:checked');
                const userAnswer = checked ? checked.value : '';
                const correctAnswer = sub_q.answer;
                const isCorrect = normalize(userAnswer) === normalize(correctAnswer);
                if (isCorrect) score++;
                results.push({ 
                    question: sub_q.question, 
                    userAnswer, 
                    correctAnswer, 
                    isCorrect, 
                    passage: q.passage 
                });
            });
        } else {
            let userAnswer = '';
            let isCorrect = false;
            let correctAnswer = q.answer;

            if (q.type === 'mcq') {
                const checked = container.querySelector('input:checked');
                userAnswer = checked ? checked.value : '';
                isCorrect = normalize(userAnswer) === normalize(correctAnswer);
            } else if (q.type === 'fill' || q.type === 'scramble' || q.type === 'writing') {
                const input = container.querySelector('input, textarea');
                userAnswer = input ? input.value.trim() : '';
                isCorrect = normalize(userAnswer) === normalize(correctAnswer);
            } else if (q.type === 'match') {
                const answerMap = JSON.parse(decodeURIComponent(container.querySelector('[data-match-map]').dataset.matchMap));
                const inputs = container.querySelectorAll('input[data-left-item]');
                let correctMatches = 0;
                let userAnswers = [];
                let correctAnswers = [];
                
                inputs.forEach(input => {
                    const leftItem = input.dataset.leftItem;
                    const userMatch = input.value.toUpperCase().trim();
                    const correctMatch = answerMap[leftItem];
                    
                    userAnswers.push(`'${leftItem}' nối với '${userMatch || '?'}'`);
                    correctAnswers.push(`'${leftItem}' nối với '${correctMatch}'`);
                    
                    if (userMatch === correctMatch) {
                        correctMatches++;
                    }
                });
                
                isCorrect = correctMatches === inputs.length;
                userAnswer = userAnswers.join(', ');
                correctAnswer = correctAnswers.join(', ');
            }
            
            if (isCorrect) score++;
            results.push({ question: q.question, userAnswer, correctAnswer, isCorrect });
        }
    });

    const scorePercent = totalQuestionsInQuiz > 0 ? (score / totalQuestionsInQuiz) : 0;
    
    // *** LOGIC MỚI: KIỂM TRA ĐỂ CẤP CHỨNG NHẬN ***
    if (isComprehensiveTest && scorePercent >= 0.8) {
        // Lấy tên và lớp từ input
        const studentName = dom.studentNameInput.value || 'Học sinh xuất sắc';
        const studentClass = dom.studentClassInput.value || 'Lớp';
        const unitName = dom.unitSelect.value;
        
        displayCertificate(studentName, studentClass, unitName);
        setUIState('certificateWrapper');
        // launchConfetti(); // (ĐÃ BỎ)
        
    } else {
        // Logic cũ: Hiển thị điểm và giải thích
        dom.score.textContent = `Bạn đã đúng ${score}/${totalQuestionsInQuiz} câu!`;
        displayFeedback(score, totalQuestionsInQuiz);
        setUIState('resultWrapper');
        displayResults(results);
        
        // Chỉ bắn pháo hoa nếu điểm cao (>= 80%) nhưng KHÔNG phải bài tổng hợp
        if (scorePercent >= 0.8) {
            // launchConfetti(); // (ĐÃ BỎ)
        }

        // Tải giải thích cho các câu sai
        results.forEach(async (res, index) => {
            if (!res.isCorrect) {
                const explanationEl = document.getElementById(`explanation-${index}`);
                if (!explanationEl) return;
                try {
                    const result = await getExplanation(res.question, res.userAnswer, res.correctAnswer);
                    explanationEl.innerHTML = `<b>Giải thích:</b> ${result.explanation}`;
                } catch (error) {
                    explanationEl.innerHTML = `Không thể tải giải thích.`;
                }
            }
        });
    }
}

/**
 * CẬP NHẬT: Reset về trang chủ
 */
function handleReset() {
    setUIState('placeholder');
    generatedQuestions = [];
    totalQuestionsInQuiz = 0;
    isComprehensiveTest = false; // Reset cờ
    // Hiện lại control panel
    dom.controlPanel.classList.remove('hidden');
}

// (TOÀN BỘ HÀM launchConfetti() ĐÃ BỊ XÓA)

/**
 * CẬP NHẬT: Luồng khởi tạo ban đầu
 */
document.addEventListener('DOMContentLoaded', () => {
    // 1. Gắn listener cho bộ chọn khối lớp
    if (dom.gradeSelect) {
        dom.gradeSelect.addEventListener('change', handleGradeChange);
    }
    
    // 2. Tải dữ liệu ban đầu (cho Lớp 5 đang được 'selected' trong HTML)
    handleGradeChange();

    // 3. Gắn các listener còn lại
    dom.generateBtn.addEventListener('click', handleGenerate);
    dom.submitBtn.addEventListener('click', handleSubmit);
    dom.resetBtn.addEventListener('click', handleReset);
    
    // GẮN LISTENER CHO NÚT MỚI
    if (dom.backToPanelBtn) {
        dom.backToPanelBtn.addEventListener('click', handleReset); 
    }

    dom.printBtn.addEventListener('click', () => window.print());
    
    // MỚI: Gắn listener cho các nút mới
    if (dom.generateComprehensiveBtn) {
        dom.generateComprehensiveBtn.addEventListener('click', handleGenerateComprehensive);
    }
    if (dom.retakeQuizBtn) {
        dom.retakeQuizBtn.addEventListener('click', handleReset);
    }
    
    // 4. Đặt trạng thái ban đầu
    setUIState('placeholder');
});