// ============================================
// 全局状态
// ============================================

let currentUsername = 'alice';
let currentUserData = null;

// ============================================
// 用户管理
// ============================================

function loadUserData() {
    const usernameInput = document.getElementById('username');
    const username = usernameInput.value.trim();

    if (!username) {
        alert('请输入用户名');
        return;
    }

    currentUsername = username;
    fetchUserData();
}

function fetchUserData() {
    fetch(`/api/user/${currentUsername}`)
        .then(response => response.json())
        .then(data => {
            currentUserData = data;
            updateUI();
        })
        .catch(error => {
            console.error('加载用户数据失败:', error);
            alert('加载用户数据失败，请确保 Flask 服务已启动');
        });
}

function updateUI() {
    if (!currentUserData) return;

    const user = currentUserData;
    document.getElementById('watched-count').textContent = user.watched.length;
    document.getElementById('watchlist-count').textContent = user.watchlist.length;
    document.getElementById('friends-count').textContent = user.friends.length;

    // 更新列表
    renderList('watched-list', user.watched);
    renderList('watchlist-list', user.watchlist);

    // 更新统计数据
    updateStats();
}

function renderList(elementId, items) {
    const list = document.getElementById(elementId);
    list.innerHTML = '';

    if (items.length === 0) {
        list.innerHTML = '<li style="color: #a0aec0; text-align: center;">暂无数据</li>';
        return;
    }

    items.forEach(item => {
        const li = document.createElement('li');
        const ratingText = item.rating ? ` ⭐${item.rating}` : '';
        li.textContent = `${item.title} (${item.genre})${ratingText}`;
        list.appendChild(li);
    });
}

// ============================================
// 统计数据
// ============================================

function updateStats() {
    // 获取平均评分
    fetch(`/api/user/${currentUsername}/avg-rating`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('avg-rating').textContent =
                data.avg_rating !== null && data.avg_rating !== undefined ?
                data.avg_rating.toFixed(1) : '-';
        })
        .catch(() => {});

    // 获取最常看类型
    fetch(`/api/user/${currentUsername}/most-genre`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('most-genre').textContent =
                data.most_watched_genre || '-';
        })
        .catch(() => {});
}

// ============================================
// Wave 1: 电影管理
// ============================================

function getMovieFromInput() {
    const title = document.getElementById('movie-title').value.trim();
    const genre = document.getElementById('movie-genre').value.trim();
    const rating = parseFloat(document.getElementById('movie-rating').value);

    if (!title || !genre || isNaN(rating) || rating < 1 || rating > 10) {
        alert('请完整填写电影信息（标题、类型、1-10 分的评分）');
        return null;
    }

    return { title, genre, rating };
}

function addMovie() {
    const movie = getMovieFromInput();
    if (!movie) return;

    fetch('/api/movie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(movie)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        alert(`✅ 电影 "${data.title}" 创建成功！`);
        // 清空输入
        document.getElementById('movie-title').value = '';
        document.getElementById('movie-genre').value = '';
        document.getElementById('movie-rating').value = '';
    })
    .catch(error => {
        alert('创建电影失败: ' + error.message);
    });
}

function addToWatched() {
    const movie = getMovieFromInput();
    if (!movie) return;

    fetch(`/api/user/${currentUsername}/watched`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        alert(`✅ ${data.message}`);
        fetchUserData();
    })
    .catch(error => {
        alert('添加到已看失败: ' + error.message);
    });
}

function addToWatchlist() {
    const movie = getMovieFromInput();
    if (!movie) return;

    fetch(`/api/user/${currentUsername}/watchlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        alert(`✅ ${data.message}`);
        fetchUserData();
    })
    .catch(error => {
        alert('添加到想看失败: ' + error.message);
    });
}

function watchMovie() {
    const title = document.getElementById('movie-title').value.trim();
    if (!title) {
        alert('请输入要标记为已看的电影名称');
        return;
    }

    fetch(`/api/user/${currentUsername}/watch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        alert(`✅ ${data.message}`);
        document.getElementById('movie-title').value = '';
        fetchUserData();
    })
    .catch(error => {
        alert('操作失败: ' + error.message);
    });
}

// ============================================
// 好友管理
// ============================================

function addFriend() {
    const friend = document.getElementById('friend-username').value.trim();
    if (!friend) {
        alert('请输入好友用户名');
        return;
    }

    fetch(`/api/user/${currentUsername}/friends`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ friend })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        alert(`✅ ${data.message}`);
        document.getElementById('friend-username').value = '';
        fetchUserData();
    })
    .catch(error => {
        alert('添加好友失败: ' + error.message);
    });
}

// ============================================
// 推荐功能
// ============================================

function showResults(title, data) {
    const container = document.getElementById('rec-results');

    if (!data || data.length === 0) {
        container.innerHTML = `<p style="color: #a0aec0;">😅 暂无推荐的电影</p>`;
        return;
    }

    let html = `<h4>${title} (${data.length} 部)</h4><ul>`;
    data.forEach(movie => {
        const ratingText = movie.rating ? ` ⭐${movie.rating}` : '';
        html += `<li>${movie.title} (${movie.genre})${ratingText}</li>`;
    });
    html += '</ul>';
    container.innerHTML = html;
}

function getUniqueWatched() {
    fetch(`/api/user/${currentUsername}/unique-watched`)
        .then(response => response.json())
        .then(data => {
            showResults('🎯 我的独享电影', data.unique_watched || []);
        })
        .catch(error => {
            alert('获取推荐失败: ' + error.message);
        });
}

function getFriendsUniqueWatched() {
    fetch(`/api/user/${currentUsername}/friends-unique-watched`)
        .then(response => response.json())
        .then(data => {
            showResults('👥 好友独享电影', data.friends_unique_watched || []);
        })
        .catch(error => {
            alert('获取推荐失败: ' + error.message);
        });
}

function getAvailableRecs() {
    fetch(`/api/user/${currentUsername}/available-recs`)
        .then(response => response.json())
        .then(data => {
            showResults('📺 订阅推荐', data.available_recs || []);
        })
        .catch(error => {
            alert('获取推荐失败: ' + error.message);
        });
}

function getRecByGenre() {
    fetch(`/api/user/${currentUsername}/rec-by-genre`)
        .then(response => response.json())
        .then(data => {
            showResults('🎭 类型推荐', data.rec_by_genre || []);
        })
        .catch(error => {
            alert('获取推荐失败: ' + error.message);
        });
}

function getRecFromFavorites() {
    fetch(`/api/user/${currentUsername}/rec-from-favorites`)
        .then(response => response.json())
        .then(data => {
            showResults('❤️ 收藏推荐', data.rec_from_favorites || []);
        })
        .catch(error => {
            alert('获取推荐失败: ' + error.message);
        });
}

// ============================================
// 初始化
// ============================================

// 页面加载时自动加载 alice 的数据
document.addEventListener('DOMContentLoaded', function() {
    fetchUserData();
});

// 支持回车键提交
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const active = document.activeElement;
        if (active.id === 'username') {
            loadUserData();
        }
    }
});