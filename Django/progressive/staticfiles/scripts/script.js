        // Create stars dynamically
        function createStars() {
            const numberOfStars = 200;

            for (let i = 0; i < numberOfStars; i++) {
                createStar();
            }
        }

        // Create a single star and append it to the body
        function createStar() {
            const star = document.createElement("div");
            star.className = "star";
            star.style.left = `${Math.random() * 100}vw`;
            star.style.top = `${Math.random() * 100}vh`;
            star.style.setProperty('--x', Math.random());
            star.style.setProperty('--y', Math.random());

            document.body.appendChild(star);
        }

        // Call the function to create stars when the page loads
        window.onload = createStars;