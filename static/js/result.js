// 页面加载完成后的处理
document.addEventListener('DOMContentLoaded', function() {
    // 为返回按钮添加点击事件
    const backButton = document.querySelector('.back-button');
    if (backButton) {
        backButton.addEventListener('click', confirmReturn);
    }
});
