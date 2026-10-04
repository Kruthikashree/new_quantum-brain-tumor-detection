import PortalLayout from "../components/PortalLayout";
import { getCurrentUser } from "../services/api";

function Profile() {
  const user = getCurrentUser();

  return (
    <PortalLayout title="Profile" subtitle="Your account details">
      <div className="pt-card">
        <div className="pt-detail">
          <div><span>Name</span><b>{user?.name}</b></div>
          <div><span>Email</span><b>{user?.email}</b></div>
          <div><span>Role</span><b>{user?.role === "doctor" ? "Doctor" : "Laboratory staff"}</b></div>
        </div>
      </div>
    </PortalLayout>
  );
}

export default Profile;