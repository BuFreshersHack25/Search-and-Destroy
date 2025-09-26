document.addEventListener('DOMContentLoaded', () => {
    const listElement = document.getElementById('leaderboard-list');
    const loader = document.getElementById('loader');
    
    // This would ideally come from your app's authentication state
    const currentUsername = "You"; 

    async function fetchLeaderboard() {
        try {
            const response = await fetch('/leaderboard_data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // Clear the loader/previous content
            listElement.innerHTML = ''; 

            if (data.length === 0) {
                listElement.innerHTML = '<div class="loader">No data available.</div>';
                return;
            }

            // Populate the list with data from the API
            data.forEach((player, index) => {
                const rank = index + 1;
                const isCurrentUser = player.username === currentUsername;

                const item = document.createElement('li');
                item.classList.add('leaderboard-item');
                if (isCurrentUser) {
                    item.classList.add('current-user');
                }

                item.innerHTML = `
                    <div class="leaderboard-rank">${rank}</div>
                    <div class="leaderboard-user">${player.username}</div>
                    <div class="leaderboard-score">${player.score.toLocaleString()}</div>
                `;
                listElement.appendChild(item);
            });

        } catch (error) {
            console.error("Failed to fetch leaderboard data:", error);
            loader.textContent = 'Failed to load leaderboard.';
        }
    }

    fetchLeaderboard();
});