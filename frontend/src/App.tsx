import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
// import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { BrowserRouter, Route, Routes } from "react-router-dom";
// import Chatbot from "@/components/chatbot/Chatbot";
import Footer from "@/components/layout/Footer";
import Navbar from "@/components/layout/Navbar";
import { useAnalytics } from "@/hooks/useAnalytics";
import Blog from "@/pages/Blog";
import BlogPost from "@/pages/BlogPost";
import Contact from "@/pages/Contact";
import Home from "@/pages/Home";
import Projects from "@/pages/Projects";
import ProjectDetail from "@/pages/ProjectDetail";
import Experience from "@/pages/Experience";
import Resume from "@/pages/Resume";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 5 * 60 * 1000, retry: 1 },
  },
});

function AppInner() {
  useAnalytics();
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/"                element={<Home />} />
        <Route path="/projects"        element={<Projects />} />
        <Route path="/projects/:slug"  element={<ProjectDetail />} />
        <Route path="/blog"            element={<Blog />} />
        <Route path="/blog/:slug"      element={<BlogPost />} />
        <Route path="/experience"      element={<Experience />} />
        <Route path="/resume"          element={<Resume />} />
        <Route path="/contact"         element={<Contact />} />
      </Routes>
      <Footer />
      {/* <Chatbot /> */}
    </>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppInner />
      </BrowserRouter>
      {/* <ReactQueryDevtools initialIsOpen={false} /> */}
    </QueryClientProvider>
  );
}