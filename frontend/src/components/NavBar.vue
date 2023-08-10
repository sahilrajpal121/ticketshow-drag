<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container-fluid">
            <!-- <a class="navbar-brand" href="/">TicketShow</a> -->
            <a href="/" type="button">
                <img src="/icons8-ticket-64.png" width="35" height="35">
            </a>
            <form class="d-flex ms-3" role="search" @submit.prevent="search">
                <input class="form-control form-control-sm me-2" type="search" placeholder="Search" aria-label="Search"
                    name="q" v-model="searchQuery">
                <button class="btn btn-secondary btn-outline-none" type="submit">
                    <img src="/search_icon.ico" alt="search" width="20" height="20">
                </button>
            </form>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li v-if="!token" class="nav-item">
                        <div class="nav-link">
                            <button class="btn btn-secondary btn-sm" style="background-color: #f84464;"
                                @click.prevent="router.push('/login')">Sign in</button>
                        </div>
                    </li>
                    <li v-else class="nav-item dropdown me-3">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            data-bs-target="#navbar" aria-expanded="false">
                            <svg width="20" height="20" viewBox="0 0 18 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" clip-rule="evenodd"
                                    d="M6.26464 4.801C6.26464 3.20871 7.55544 1.91791 9.14772 1.91791C10.74 1.91791 12.0308 3.20872 12.0308 4.801C12.0308 6.39329 10.74 7.68409 9.14772 7.68409C7.55544 7.68409 6.26464 6.39329 6.26464 4.801ZM9.14772 0.5C6.77234 0.5 4.84673 2.42563 4.84673 4.801C4.84673 7.17637 6.77234 9.102 9.14772 9.102C11.5231 9.102 13.4487 7.17638 13.4487 4.801C13.4487 2.42562 11.5231 0.5 9.14772 0.5ZM2.10541 16.3333C2.10541 13.7077 4.33249 11.4652 7.0681 11.4652H11.3218C14.0653 11.4652 16.2845 13.6209 16.2845 16.3333V17.1405C16.2089 17.6863 15.7974 18.0821 15.292 18.0821H3.00342C2.51666 18.0821 2.10541 17.7108 2.10541 17.1841V16.3333ZM7.0681 10.0473C3.5649 10.0473 0.6875 12.9092 0.6875 16.3333V17.1841C0.6875 18.5479 1.78868 19.5 3.00342 19.5H15.292C16.6665 19.5 17.5717 18.4003 17.6981 17.2624C17.701 17.2364 17.7024 17.2102 17.7024 17.1841V16.3333C17.7024 12.8069 14.8172 10.0473 11.3218 10.0473H7.0681Z"
                                    fill="white"></path>
                            </svg>
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <a class="dropdown-item" href="/">Signed in as
                                    <br><strong>{{decodeToken(token).email}}</strong>
                                </a>
                            </li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a class="dropdown-item" href="/bookings">Bookings</a></li>
                            <li><a class="dropdown-item" href="/">Export Blogs</a></li>
                            <li><a class="dropdown-item" href="/">Change Password</a></li>
                            <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#DeleteAccount"
                                    href="#">Delete
                                    account</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a type="button" class="dropdown-item" @click.prevent="logout()">Sign out</a></li>
                        </ul>
                    </li>
                </ul>




            </div>
        </div>
    </nav>
    <div class="modal fade" id="DeleteAccount" tabindex="-1" aria-labelledby="DeleteAccountBody" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="DeleteAccountBody">Confirm?</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Are you sure you want to delete the account?
                    <br>This cannot be undone.
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <a class="btn btn-danger" href="/">Delete</a>
                </div>
            </div>
        </div>
    </div>
    <br><br><br>
</template>

<script setup>

import { useRouter } from "vue-router";
import { ref } from "vue";
import { logout, decodeToken, getToken } from "../helpers/authHelper";

const token = getToken();

const router = useRouter();
const searchQuery = ref('')

const search = () => {
    if (searchQuery.value) {
        router.push({ path: "/search", query: { q: searchQuery.value } });
    } else {
        router.push({ path: "/" });
    }
};

</script>


<style scoped>
.css-1dknsd1 {
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-align-items: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    height: 38px;
    width: 40px;
    margin-right: 15px;
    background: transparent;
    border-radius: 100px;
    color: white;
    font-weight: 600;
    font-size: 13px;
    line-height: 150%;
    cursor: pointer;
    border: 1px solid rgba(255, 255, 255, 0.2);
    -webkit-transition: box-shadow 0.3s;
    transition: box-shadow 0.3s;
    -webkit-box-pack: center;
    -webkit-justify-content: center;
    -ms-flex-pack: center;
    justify-content: center;
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
}

.css-1dknsd1:hover {
    border: 1px solid white;
}

@media screen and (max-width: 768px) {
    .css-1dknsd1 {
        display: none;
    }
}
</style>